from itertools import chain
import json
import logging
import operator
import os
from pathlib import Path
from time import time
import typing
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Type, Union

from furiosa_torch_ext.torch_ext import SIDE_EFFECT_OPS
import torch
from torch.fx import Graph, GraphModule, Node
from torch.fx.node import _side_effectful_functions
from torch.utils._pytree import tree_flatten
from transformers import PretrainedConfig

from furiosa_llm.hash import get_env_independent_hash, hash_example_inputs, hash_model
from furiosa_llm.parallelize.pipeline_builder.export import save_tensors
from furiosa_llm.parallelize.pipeline_builder.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.pipeline_builder.trace import get_aten_graph_with_original_names

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata

from furiosa_llm.parallelize.block_slicer import (
    get_block_slicing_edges,
    get_blockwise_sliced_color_map,
)
from furiosa_llm.parallelize.config import Device, MpppConfig
from furiosa_llm.parallelize.model_rewriter.model_rewriter import ModelRewriter
from furiosa_llm.parallelize.model_rewriter.ops import custom_ops  # noqa: F401
from furiosa_llm.parallelize.model_rewriter.utils import get_fake_mode
from furiosa_llm.parallelize.mppp.mppp import Mppp
from furiosa_llm.parallelize.node_meta import (
    QParamKind,
    get_color,
    get_original_name,
    get_qparam_kind,
    has_original_name,
    set_color,
    set_original_name,
    set_to_be_embedded,
    set_unsharded_tensor_meta,
)
from furiosa_llm.parallelize.pipeline.types import (
    MetadataTensor,
    MetadataTensorSlice,
    ParamfileFormat,
    ParamFileInfo,
    ParamInfo,
    Pipeline,
    SuperTaskKind,
)
from furiosa_llm.parallelize.pipeline_builder.converter import (
    ADDITIONAL_PARAM_FILE_ID,
    DEFAULT_PARAM_FILE_ID,
    GraphModuleConverter,
    _tensor_exists_in_file,
)
from furiosa_llm.parallelize.pipeline_builder.utils import (
    get_constant_tensors_with_original_name,
    get_saved_param_names,
    write_without_concurrency_issue,
)
from furiosa_llm.parallelize.utils import (
    get_original_model_type,
    is_aten_op,
    is_custom_op,
    is_kvcache,
)
from furiosa_llm.utils import get_cache_path_if_exists

if typing.TYPE_CHECKING:
    from furiosa_llm.compiler_config import CompilerConfigContext


logger = logging.getLogger(__file__)


def _get_sliced_torch_where_get_attr_nodes(gm: GraphModule) -> Tuple[Node, ...]:
    """Find get_attr nodes if it's used as ``torch.ops.aten.where``'s condition tensor (first input tensor) after a slice opertion."""

    cache = set()
    to_be_embedded = set()
    for node in gm.graph.nodes:
        if not (node.op == "call_function" and node.target == torch.ops.aten.where.self):
            continue

        queue: List[Tuple[Node, bool]] = [(node.args[0], False)]

        while queue:
            node, found_slice = queue.pop()
            if node.op == "get_attr" and found_slice:
                to_be_embedded.add(node)
                continue
            flattened_args, _ = tree_flatten((node.args, node.kwargs))
            for arg in flattened_args:
                if not isinstance(arg, Node) or arg in cache:
                    continue
                cache.add(arg)
                queue.append((arg, found_slice or arg.target == torch.ops.aten.slice.Tensor))
    return tuple(to_be_embedded)


def _get_zero_point_for_dpe_qparam_nodes(gm: GraphModule) -> Tuple[Node, ...]:
    """Get zero point qparam get_attr nodes running on DPE."""
    zp_for_dpe_nodes = tuple(
        node
        for node in gm.graph.nodes
        if node.op == "get_attr" and get_qparam_kind(node) == QParamKind.ZERO_POINT_FOR_DPE
    )

    for node in zp_for_dpe_nodes:
        actual_tensor = getattr(gm, node.target)
        # This assumption is not valid for fp8 models.
        if actual_tensor.dim() != 0 and tuple(actual_tensor.shape) != (1,):
            raise RuntimeError(
                f"Non-sclar dpe zero-point qparam {node.name} found, all dpe zero-point qparams should be sclar tensors for compilation."
            )
        if actual_tensor.count_nonzero() > 0:
            # TODO: remove this after compiler issue is fixed.
            logging.warning(
                f"non-zero dpe zero-point qparam found: {node.name}, this may cause inefficient compilation."
            )

    return zp_for_dpe_nodes


def _mark_constants_to_be_embedded(gm: GraphModule) -> None:
    """Mark some constants (get_attr nodes) to be embedded in FX graph as it is."""
    for node in _get_sliced_torch_where_get_attr_nodes(gm) + _get_zero_point_for_dpe_qparam_nodes(
        gm
    ):
        set_to_be_embedded(node)


def _get_commit_id() -> str:
    import git  # type: ignore

    repo = git.Repo(Path(__file__).parent, search_parent_directories=True)
    return repo.head.object.hexsha


def _add_block_id_info(
    original_model_type: Type,
    aten_gm: GraphModule,
    num_blocks_per_supertask: int,
) -> None:
    """Add block id info for nodes in ``aten_gm``."""
    slicing_edges = get_block_slicing_edges(aten_gm, original_model_type)

    # Get block id map for nodes. Nodes with same block id belongs to same block.
    get_blockwise_sliced_color_map(aten_gm, slicing_edges, mark_color_to_meta=True)

    # Cahnge block ids according to `num_blocks_per_supertask``.
    for node in aten_gm.graph.nodes:
        colors = get_color(node)
        if colors is None:
            continue
        new_colors = [color // num_blocks_per_supertask for color in colors]
        set_color(node, new_colors)


ANONYMOUS_CONSTANT_NAME_PREFIX = "ANONYMOUS_CONSTANT_"


def _add_original_name_to_anonymous_get_attr_nodes(gm: GraphModule) -> None:
    existing_original_names = set(
        get_original_name(node) for node in gm.graph.nodes if has_original_name(node)
    )
    for idx, node in enumerate(gm.graph.nodes):
        if node.op != "get_attr" or has_original_name(node):
            continue
        constant_name = f"{ANONYMOUS_CONSTANT_NAME_PREFIX}{idx}"
        assert (
            constant_name not in existing_original_names
        ), f"constant name {constant_name} already exists in the model."
        set_original_name(node, constant_name)


def _get_input_ids_batch_size(graph: Graph) -> int:
    input_ids_node = tuple(
        node
        for node in graph.nodes
        if node.op == "placeholder"
        and has_original_name(node)
        and get_original_name(node) == "input_ids"
    )
    if len(input_ids_node) != 1:
        raise ValueError("Multiple input id nodes exist. This is different from expected.")
    input_ids_shape = input_ids_node[0].meta["tensor_meta"].shape
    if len(input_ids_shape) != 2:
        raise ValueError("Input ids shape is different from expected.")
    return input_ids_shape[0]


def _get_index_batch_size_for_beam_search_kv_cache_sharing_model(
    index_op_node: Node, input_ids_batch_size: int
) -> int:
    assert index_op_node.target == torch.ops.aten.index.Tensor

    # Find first concatenation which concats past k/v cache with newly generated k/v.
    cur = index_op_node
    while True:
        if len(cur.users) != 1:
            raise ValueError(
                "Unexpected pattern. We expect concatenated k/v to be 4-dimensional tensor."
            )
        child = next(iter(cur.users))
        if child.target == torch.ops.aten.cat.default:
            break
        cur = child

    concatenated_shape = child.meta["tensor_meta"].shape
    if len(concatenated_shape) != 4:
        raise ValueError(
            "Unexpected pattern. We expect concatenated k/v to be 4-dimensional tensor."
        )

    # Assume sequence length doesn't change from index to concat.
    k_or_v_cache_shape_before_concat = cur.meta["tensor_meta"].shape
    mul_of_batch_size_and_seq_length_before_concat = (
        k_or_v_cache_shape_before_concat[0] * k_or_v_cache_shape_before_concat[1]
    )
    if mul_of_batch_size_and_seq_length_before_concat % input_ids_batch_size != 0:
        raise ValueError(
            "Unexpected pattern. We expect batch size and sequence length to be first two dimensions of k/v cache (Order doesn't matter)."
        )

    seq_length = mul_of_batch_size_and_seq_length_before_concat // input_ids_batch_size

    index_output_shape = index_op_node.meta["tensor_meta"].shape
    mul_of_batch_size_and_seq_length_after_index = index_output_shape[0] * index_output_shape[1]

    if mul_of_batch_size_and_seq_length_after_index % seq_length != 0:
        raise ValueError(
            "Unexpected pattern. We expect multiplication of index output tensor's first two dimensions eqauls to multiplication of batch size and sequence length."
        )
    return mul_of_batch_size_and_seq_length_after_index // seq_length


def _replace_paged_attention_index_ops_with_furiosa_sparse_index(
    graph: Graph,
    dummy_index: int,
    model_use_beam_search_kv_cache_sharing: bool,
    sparse_select_version: str,
) -> None:
    input_ids_batch_size = _get_input_ids_batch_size(graph)

    index_op_nodes = [node for node in graph.nodes if node.target == torch.ops.aten.index.Tensor]

    if model_use_beam_search_kv_cache_sharing:
        # To ensure `past_valid_key_prompt_indices` indexing nodes goes before `past_valid_key_decode_indices` indexing nodes.
        index_op_nodes.sort(key=lambda node: node.args[1][0].name)

    prompt_batch_size = None

    for node in index_op_nodes:
        input_tensor = node.args[0]

        found = False
        queue = [input_tensor]

        # Check index op node is one for kv cache indexing.
        while queue:
            next_ = queue.pop()
            if next_.op == "placeholder" and is_kvcache(get_original_name(next_)):
                # Assume dimension of total kv cache space is 4
                if len(next_.meta["tensor_meta"].shape) != 4:
                    raise ValueError(
                        "Unexpected pattern: input kv cache tensor should be 4-dimensional."
                    )
                # If kv cache total space is its ancestor, we consider this index op as one for paged attention indexing.
                found = True
                break
            args, _ = tree_flatten((next_.args, next_.kwargs))
            for arg in args:
                if not isinstance(arg, Node):
                    continue
                queue.append(arg)

        if found:
            indices = node.args[1]
            if len(indices) != 1:
                raise NotImplementedError("We only consider index ops with single index tensor.")
            index_shape = indices[0].meta["tensor_meta"].shape
            assert len(index_shape) == 1

            if model_use_beam_search_kv_cache_sharing:
                batch_size = _get_index_batch_size_for_beam_search_kv_cache_sharing_model(
                    node, input_ids_batch_size
                )
                if input_ids_batch_size == batch_size:
                    # indexing for "past_valid_{key|value}_decode"s
                    assert prompt_batch_size is not None
                    beam_width = batch_size // prompt_batch_size
                else:
                    # indexing for "past_valid_{key|value}_prompt"s
                    if prompt_batch_size is None:
                        prompt_batch_size = batch_size
                    else:
                        if prompt_batch_size != batch_size:
                            raise ValueError(
                                "Unexpected pattern: batch sizes of all past_valid_{key|value}_prompt tensors should be same."
                            )
                    beam_width = 1
            else:
                batch_size = input_ids_batch_size
                beam_width = 1

            assert index_shape[0] % batch_size == 0
            kv_cache_length_per_batch = index_shape[0] // batch_size

            # change node target and args to furiosa.sparse_select
            assert len(node.args) == 2
            if sparse_select_version == "v1.0":
                node.target = torch.ops.furiosa.sparse_select.default
                node.args = (*node.args, dummy_index, kv_cache_length_per_batch)
            elif sparse_select_version == "v1.5":
                node.target = torch.ops.furiosa.sparse_select_v1_5.default
                node.args = (*node.args, dummy_index, kv_cache_length_per_batch, beam_width)
            else:
                raise ValueError(f"Invalid sparse_select_version: {sparse_select_version}")


class PipelineBuilder:
    model: Union[torch.nn.Module, ModelCreationInfo]
    model_config: Optional[PretrainedConfig]
    dyn_shape_gms: Dict[str, GraphModule]

    def __init__(
        self,
        model: Union[torch.nn.Module, ModelCreationInfo],
        model_config: Optional[PretrainedConfig],
        tmp_dir: os.PathLike,
        is_beam_search_kv_cache_sharing_model: bool,
    ):
        self.model = model
        self.model_config = model_config
        self.tmp_dir = Path(tmp_dir)
        self.is_beam_search_kv_cache_sharing_model = is_beam_search_kv_cache_sharing_model
        self.dyn_shape_gms = {}

    def __gen_pipepline_hash(
        self,
        example_args: Sequence[Any],
        example_kwargs: Dict[str, Any],
        mppp_config: MpppConfig,
        param_info: ParamFileInfo,
        comp_supertask_kind: SuperTaskKind,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        padding_block_idx: Optional[int],
        sparse_select_version: str,
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
    ) -> str:
        if isinstance(self.model, ModelCreationInfo):
            original_model_type = self.model.metadata.get_optimized_cls()
            model_config = self.model.metadata.config
            qformat_qparam_path = self.model.get_qparam_qformat_path()
            seed = self.model.seed
            is_random_weight_model = self.model.random_weight_model
        else:
            # TODO
            raise NotImplementedError("Don't support pipeline hashing for non-metadata models.")

        saved_param_names = get_saved_param_names(param_info)
        saved_param_names.sort()

        to_be_hashed = (
            _get_commit_id(),
            hash_model(
                original_model_type,
                model_config,
                qformat_qparam_path,
                model_config.name_or_path,
                seed,
                is_random_weight_model,
            ),
            hash_example_inputs(example_args, example_kwargs),
            mppp_config.to_json(),
            json.dumps(saved_param_names),
            str(comp_supertask_kind),
            str(use_blockwise_compile),
            str(do_decompositions_for_model_rewrite),
            str(padding_block_idx),
            str(num_blocks_per_supertask),
            str(embed_all_constants_into_graph),
            sparse_select_version,
        )

        return get_env_independent_hash(to_be_hashed)

    @staticmethod
    def __is_aten_graph(graph: Graph) -> bool:
        return all(
            node.op in ("placeholder", "get_attr", "output")
            or (
                node.op == "call_function"
                and (
                    is_aten_op(node.target)
                    or is_custom_op(node.target)
                    or node.target == operator.getitem
                )
            )
            for node in graph.nodes
        )

    @staticmethod
    def __add_unsharded_tensor_meta(
        graph: Graph,
    ):
        # store unsharde shape info for placeholder/output nodes.
        for node in graph.nodes:
            if node.op == "placeholder":
                set_unsharded_tensor_meta(node, node.meta["tensor_meta"])
            elif node.op == "output":
                set_unsharded_tensor_meta(
                    node, tuple(arg.meta["tensor_meta"] for arg in node.args[0])
                )

    def __additional_param_file_path(self, pipeline_name: str) -> Path:
        return self.tmp_dir / f"add_const_file-{pipeline_name}.safetensors"

    def save_additional_params(
        self,
        example_args: Sequence[Any],
        example_kwargs: Dict[str, Any],
        file_path: os.PathLike,
        target_params: Sequence[str],
        save_format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
        cache_dir: Optional[os.PathLike] = None,
    ) -> None:
        """Save parameters in ``model``, but not in ``excludes`` to ``file_path``."""
        assert not os.path.exists(file_path)

        # Some additional params appear in aten-level, so lower it to aten level.
        aten_gm = get_aten_graph_with_original_names(
            self.model,
            example_args,
            example_kwargs,
            cache_dir=cache_dir,
            dynamic_shape_torch_ir_gm_store=self.dyn_shape_gms,
        )[0]

        _add_original_name_to_anonymous_get_attr_nodes(aten_gm)

        all_tensor_constants = get_constant_tensors_with_original_name(aten_gm)
        constants_to_be_saved = {name: all_tensor_constants[name] for name in target_params}

        # Save additional params to ``file_path`` if exists.
        if constants_to_be_saved:
            save_tensors(constants_to_be_saved, file_path, save_format)

    def __gen_pipeline(
        self,
        pipeline_name: str,
        example_args: Sequence[Any],
        example_kwargs: Dict[str, Any],
        mppp_config: MpppConfig,
        param_file_info: ParamFileInfo,
        export_path: Optional[Path],
        comp_supertask_kind: SuperTaskKind,
        # current context: model_qname, beam_size, phase, bucket
        compiler_config_context: "CompilerConfigContext",
        input_names: Optional[Sequence[str]],
        output_names: Optional[Sequence[str]],
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        padding_block_idx: Optional[int],
        sparse_select_version: str,
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        cache_dir: Optional[os.PathLike],
    ) -> Pipeline:
        if aten_gm := getattr(self, "aten_gm", None):
            pass
        else:
            aten_gm = get_aten_graph_with_original_names(
                self.model,
                example_args,
                example_kwargs,
                input_names=input_names,
                output_names=output_names,
                do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
                cache_dir=cache_dir,
                dynamic_shape_torch_ir_gm_store=self.dyn_shape_gms,
            )[0]

        logger.info("Add metadata and rewrite fx graph.")
        start = time()

        # What we want to do is to prevent only side-effect ops with no user from being eliminated by dead code elimination.
        # But union of ``_side_effectful_functions`` and ``SIDE_EFFECT_OPS`` contains only some of those side-effect ops.
        # TODO: Find a way to get a list of all side-effect aten ops.
        for node in aten_gm.graph.nodes:
            if (
                node.op != "output"
                and len(node.users) == 0
                and node.target not in _side_effectful_functions.union(SIDE_EFFECT_OPS)
            ):
                logging.warning(
                    f"Node with no user found, this might means meaningful nodes can disappear during postprocess: {node}"
                )

        assert PipelineBuilder.__is_aten_graph(aten_gm.graph)

        # Add original name for anonymous get_attr nodes, which are not given name by `add_original_name_info` and `add_qparam_info`.
        _add_original_name_to_anonymous_get_attr_nodes(aten_gm)

        # mark some tensor constants (get_attr nodes) to be embedded in FX graph as it is
        # (instead of converting them as placeholders in future stages).
        _mark_constants_to_be_embedded(aten_gm)

        if padding_block_idx is not None:
            _replace_paged_attention_index_ops_with_furiosa_sparse_index(
                aten_gm.graph,
                padding_block_idx,
                self.is_beam_search_kv_cache_sharing_model,
                sparse_select_version,
            )

        # Get constants that are not saved in given parameter file.
        # This will be passed to PipelineConverter.
        constants_not_in_param_file = get_constant_tensors_with_original_name(
            aten_gm,
        )

        # Exclude already saved ones
        for name in get_saved_param_names(param_file_info):
            constants_not_in_param_file.pop(name, None)

        # Save parameters not in parameter saved file referenced by ``param_file_info`` (e.g., qparam).
        additional_param_file_info = ParamFileInfo(
            str(self.__additional_param_file_path(pipeline_name)), ParamfileFormat.SAFETENSORS
        )

        PipelineBuilder.__add_unsharded_tensor_meta(aten_gm.graph)

        fake_mode = get_fake_mode(chain(aten_gm.parameters(), aten_gm.buffers()))
        fake_args_for_aten_gm = tuple(
            fake_mode.from_tensor(node.meta["val"])
            for node in aten_gm.graph.nodes
            if node.op == "placeholder"
        )

        if use_blockwise_compile:
            if isinstance(self.model, ModelCreationInfo):
                original_model_type = self.model.metadata.get_optimized_cls()
            else:
                assert isinstance(self.model, torch.nn.Module)
                original_model_type = get_original_model_type(self.model)

            # Add block id information for nodes if possible.
            _add_block_id_info(original_model_type, aten_gm, num_blocks_per_supertask)

        model_rewriter = ModelRewriter(aten_gm, mppp_config)

        rewritten_model = model_rewriter.rewrite(fake_args_for_aten_gm)

        logger.info("Adding metadata and rewriting fx graph took %.2f seconds.", time() - start)

        start = time()
        pipeline = GraphModuleConverter(
            rewritten_model,
            mppp_config.devices,
            model_rewriter.get_device_id_map(),
        ).convert(
            pipeline_name,
            param_file_info,
            comp_supertask_kind,
            compiler_config_context,
            one_supertask_per_device,
            additional_param_file_info,
            constants_not_in_param_file,
            use_blockwise_compile,
            embed_all_constants_into_graph,
        )
        logger.info("Converting GraphModule to pipeline took %.2f seconds.", time() - start)

        if export_path is not None:
            write_without_concurrency_issue(pipeline.to_json(), export_path)

        return pipeline

    @staticmethod
    def __replace_original_tensor_names(
        origin: MutableMapping[str, MetadataTensor],
        slices: Mapping[str, MetadataTensorSlice],
        new_names: Sequence[str],
    ) -> bool:
        need_resave = False
        replace_map = {}

        # Find original tensor names that need to be replaced.
        for cur_name, original_tensor_info in tuple(origin.items()):
            new_name = new_names[original_tensor_info.idx]
            if cur_name != new_name:
                origin[new_name] = original_tensor_info
                need_resave = True
                replace_map[cur_name] = new_name

        # Replace original tensor names in tensor slices.
        for tensor_slice_meta in slices.values():
            if tensor_slice_meta.origin in replace_map:
                tensor_slice_meta.origin = replace_map[tensor_slice_meta.origin]
        return need_resave

    def build(
        self,
        pipeline_name: str,
        devices: Sequence[Device],
        example_args: Sequence[Any],
        example_kwargs: Dict[str, Any],
        mppp_or_mppp_config: Union[MpppConfig, Mppp],
        param_info: ParamFileInfo,
        # current context: model_qname, beam_size, phase, bucket
        compiler_config_context: "CompilerConfigContext",
        comp_supertask_kind: SuperTaskKind = SuperTaskKind.FX,
        input_names: Optional[Sequence[str]] = None,
        output_names: Optional[Sequence[str]] = None,
        cache_dir: Optional[Path] = None,
        one_supertask_per_device: bool = False,
        use_blockwise_compile: bool = False,
        do_decompositions_for_model_rewrite: bool = False,
        padding_block_idx: Optional[int] = None,
        sparse_select_version: str = "v1.5",
        embed_all_constants_into_graph: bool = False,
        num_blocks_per_supertask: int = 1,
    ) -> Pipeline:
        if isinstance(mppp_or_mppp_config, Mppp):
            # Original name information might be needed for mppp config generation (e.g., block slicer).
            self.aten_gm = get_aten_graph_with_original_names(
                self.model,
                example_args,
                example_kwargs,
                input_names=input_names,
                output_names=output_names,
                do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
                cache_dir=cache_dir,
                dynamic_shape_torch_ir_gm_store=self.dyn_shape_gms,
            )[0]
            model: Union["ModelMetadata", torch.nn.Module]
            if isinstance(self.model, ModelCreationInfo):
                model = self.model.metadata
            else:
                assert isinstance(self.model, torch.nn.Module)
                model = self.model
            mppp_config = mppp_or_mppp_config.gen_config(
                model,
                self.model_config,
                devices,
                example_args,
                example_kwargs,
                graph_module=self.aten_gm,
            )
        else:
            mppp_config = mppp_or_mppp_config

        # We cache models only if model is `ModelCreationInfo` now.
        # TODO: add caching support for ordinary nn.Module.
        if (
            cache_dir is not None
            and isinstance(self.model, ModelCreationInfo)
            and self.model.is_hashable()
        ):
            # name is not used for hashing because it doesn't affect other fields of pipeline.
            pipeline_hash = self.__gen_pipepline_hash(
                example_args,
                example_kwargs,
                mppp_config,
                param_info,
                comp_supertask_kind,
                use_blockwise_compile,
                do_decompositions_for_model_rewrite,
                padding_block_idx,
                sparse_select_version,
                embed_all_constants_into_graph,
                num_blocks_per_supertask,
            )
            need_resave = False
            need_additional_param_save = False  # whether parameters not in parameter file referenced by ``param_info`` exists.
            additional_params_to_be_saved = []
            additional_param_file_path = self.__additional_param_file_path(pipeline_name)
            export_path = cache_dir / "pipelines" / f"{pipeline_name}-{pipeline_hash}.json"
            os.makedirs(cache_dir / "pipelines", exist_ok=True)

            cached_pipeline_path = get_cache_path_if_exists(pipeline_hash, "json", cache_dir)

            if cached_pipeline_path:
                # cached pipeline exists.
                cached_pipeline = Pipeline.load(cached_pipeline_path)
                if cached_pipeline.name != pipeline_name:
                    need_resave = True
                    cached_pipeline.name = pipeline_name

                if input_names is not None:
                    need_resave &= PipelineBuilder.__replace_original_tensor_names(
                        cached_pipeline.metadata.tensors.inputs,
                        cached_pipeline.metadata.tensor_slices.inputs,
                        input_names,
                    )
                if output_names is not None:
                    need_resave &= PipelineBuilder.__replace_original_tensor_names(
                        cached_pipeline.metadata.tensors.outputs,
                        cached_pipeline.metadata.tensor_slices.outputs,
                        output_names,
                    )

                for tensor_info in cached_pipeline.tensors.values():
                    if not isinstance(tensor_info, ParamInfo):
                        continue
                    cached_param_file_info = cached_pipeline.param_files[
                        tensor_info.value.param_file
                    ]
                    if cached_param_file_info != param_info:
                        # Different param file is used.
                        need_resave = True
                        if _tensor_exists_in_file(tensor_info.value.name, param_info):
                            # check given param file has same param names as
                            # param file used for cached pipeline
                            tensor_info.value.param_file = DEFAULT_PARAM_FILE_ID
                        else:
                            # This param doesn't exist in given param file. Add this to  ``additional_params_to_be_saved``.
                            tensor_info.value.param_file = ADDITIONAL_PARAM_FILE_ID
                            need_additional_param_save = True
                            additional_params_to_be_saved.append(tensor_info.value.name)

                cached_pipeline.param_files[DEFAULT_PARAM_FILE_ID] = param_info
                save_format = ParamfileFormat.SAFETENSORS
                cached_pipeline.param_files[ADDITIONAL_PARAM_FILE_ID] = ParamFileInfo(
                    os.fspath(additional_param_file_path), save_format
                )

                if need_additional_param_save:
                    self.save_additional_params(
                        example_args,
                        example_kwargs,
                        additional_param_file_path,
                        additional_params_to_be_saved,
                        save_format,
                        cache_dir=cache_dir,
                    )

                # if name, param info or input/output names is different from cached one,
                # reexport the pipeline.
                if need_resave:
                    write_without_concurrency_issue(cached_pipeline.to_json(), export_path)

                return cached_pipeline
        else:
            # don't cache
            export_path = None

        # Don't cache if comp_supertask_kind != "fx" because other formats
        # cannot be serialized properly.
        # FIXME: cache other formats after fixing issues.
        if comp_supertask_kind != "fx":
            export_path = None

        return self.__gen_pipeline(
            pipeline_name,
            example_args,
            example_kwargs,
            mppp_config,
            param_info,
            export_path,
            comp_supertask_kind,
            compiler_config_context,
            input_names,
            output_names,
            one_supertask_per_device,
            use_blockwise_compile,
            do_decompositions_for_model_rewrite,
            padding_block_idx,
            sparse_select_version,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            cache_dir=cache_dir,
        )
