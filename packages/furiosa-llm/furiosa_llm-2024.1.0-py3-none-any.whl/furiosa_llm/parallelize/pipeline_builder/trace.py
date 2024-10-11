from collections import defaultdict
import copy
import inspect
from itertools import chain
import logging
import operator
import os
from pathlib import Path
from time import time
import typing
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata

import furiosa_llm_models
from furiosa_torch_ext.torch_ext import eliminate_dead_code
from more_itertools import zip_equal
import torch
from torch._dispatch.python import enable_python_dispatcher
from torch._dynamo.source import GetItemSource, LocalSource
from torch._guards import Source
from torch._subclasses.fake_tensor import FakeTensor
from torch.export import dynamic_dim
import torch.fx
from torch.fx import Graph, GraphModule, Node, map_arg
from torch.fx.experimental.proxy_tensor import make_fx
from torch.fx.node import has_side_effect
from torch.overrides import TorchFunctionMode
from torch.utils._pytree import tree_flatten, tree_map_only

from furiosa_llm.hash import get_env_independent_hash, hash_example_inputs, hash_model
from furiosa_llm.parallelize.model_rewriter.utils import get_fake_mode
from furiosa_llm.parallelize.node_meta import (
    fill_tensor_meta_from_val_meta,
    get_original_name,
    has_original_name,
)
from furiosa_llm.parallelize.pipeline_builder.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.pipeline_builder.original_node_mapper import (
    add_original_name_info,
    add_qparam_info,
)
from furiosa_llm.parallelize.pipeline_builder.serialize import load_gm, save_gm
from furiosa_llm.parallelize.pipeline_builder.transform import decompose_layernorm, decompose_linear
from furiosa_llm.parallelize.utils import (
    flatten_input_tensors,
    get_original_model_type,
    get_output_names,
    is_typecast_node,
)
from furiosa_llm.quantized_models import QuantCausalLM
from furiosa_llm.utils import get_cache_path_if_exists

# Model tracer version
TRACER_VERSION = "0.2.0"
logger = logging.getLogger(__file__)


class FakeCopyModeWithMapping(TorchFunctionMode):
    """When `self.fake_to_real` is False, this converts all real tensors in objects to fake ones, maintaining a mapping from fake tensor to real tensor.
    Otherwise, this converts all fake tensors in objects to original real ones using previously saved mapping.
    """

    def __init__(self, fake_mode):
        self.fake_mode = fake_mode
        self.fake_tensor_to_real = {}
        self.fake_to_real = False

    def set_fake_to_real(self, val: bool) -> None:
        self.fake_to_real = val

    def _handle_tensor(self, input_tensor: torch.Tensor) -> torch.Tensor:
        if self.fake_to_real:
            if isinstance(input_tensor, FakeTensor):
                # Convert fake tensor to its original real tensor.
                new_tensor = self.fake_tensor_to_real[input_tensor]
            else:
                # This tensor is real tensor which does not exist before tracing, but created dynamicall.
                # Just return this as it is.
                new_tensor = input_tensor
        else:
            if isinstance(input_tensor, FakeTensor):
                # This tensor is originally fake tensor.
                new_tensor = input_tensor
                self.fake_tensor_to_real[input_tensor] = input_tensor
            else:
                # Create fake tensor from real tensor.
                new_tensor = self.fake_mode.from_tensor(input_tensor, static_shapes=True)
            self.fake_tensor_to_real[new_tensor] = input_tensor
        return new_tensor

    def __torch_function__(self, func, types, args=(), kwargs=None):
        kwargs = kwargs if kwargs else {}

        # clone will get called in Parameter deepcopy
        if func == torch._C._TensorBase.clone:
            to_be_cloned = args[0]
            new_tensor = self._handle_tensor(to_be_cloned)
            return func(new_tensor, **kwargs)
        elif func == torch.Tensor.__deepcopy__:
            assert len(args) == 2 and len(kwargs) == 0
            tensor, memo = args

            if id(tensor) in memo:
                return memo[id(tensor)]

            out = self._handle_tensor(tensor)
            memo[id(tensor)] = out
            return out
        else:
            with torch._C.DisableTorchFunctionSubclass():
                return func(*args, **kwargs)


def _remove_duplicate_typecasts(graph: Graph) -> None:
    for node in graph.nodes:
        if not is_typecast_node(node):
            continue

        dtype = node.meta["tensor_meta"].dtype

        to_searches = list(node.users)

        while to_searches:
            child = to_searches.pop()
            if not is_typecast_node(child) or child.meta["tensor_meta"].dtype != dtype:
                continue
            to_searches.extend(child.users)
            child.replace_all_uses_with(node)
            graph.erase_node(child)


def _merge_duplicate_descendants(node: Node, gm: GraphModule) -> None:
    cur = node

    while True:
        children = tuple(cur.users.keys())
        if len(children) == 0:
            return
        elif len(children) == 1:
            cur = children[0]
            continue
        else:
            first_child = children[0]
            if not all(
                first_child.args == child.args and first_child.kwargs == child.kwargs
                for child in children[1:]
            ):
                # Children are not identical. Just stop here.
                return

            # All children are identical. Remove duplicates and leave just one of them.
            representative_child = children[0]

            for duplicate_child in children[1:]:
                duplicate_child.replace_all_uses_with(representative_child)
                gm.graph.erase_node(duplicate_child)
            cur = representative_child


# FIXME: this function is highly coupled with mlperf submission slice model.
def _make_quantized_gptj_mlperf_slice_prefill_model_slicable(
    gm: GraphModule,
) -> None:
    targets = [
        node
        for node in gm.graph.nodes
        if node.op == "placeholder"
        and get_original_name(node) in ("position_ids", "new_key_location", "new_value_location")
    ]

    # position_ids: placeholder - unsqueeze - repeat - gather
    # new_key_location, new_value_location: placeholder - reshape - squeeze - index_put
    for target in targets:
        _merge_duplicate_descendants(target, gm)


def _remove_unnecessary_larger_typecast_before_index(graph: Graph) -> None:
    for node in graph.nodes:
        if node.op != "call_function" or node.target != torch.ops.aten.index.Tensor:
            continue
        indices = node.args[1]
        if len(indices) != 1:
            raise NotImplementedError("We only consider index ops with single index tensor now.")
        index = indices[0]
        if is_typecast_node(index) and index.meta["tensor_meta"].dtype == torch.int64:
            assert len(index.all_input_nodes) == 1
            node_before_conversion = index.all_input_nodes[0]
            dtype_before_cast = node_before_conversion.meta["tensor_meta"].dtype
            if (
                not dtype_before_cast.is_floating_point
                and torch.iinfo(dtype_before_cast).bits < torch.iinfo(torch.int64).bits
            ):
                index.replace_all_uses_with(node_before_conversion)
                graph.erase_node(index)


def _check_all_index_ops_i32_index(graph: Graph) -> None:
    for node in graph.nodes:
        if not (
            node.op == "call_function"
            and node.target in (torch.ops.aten.index.Tensor, torch.ops.aten.index_put_.default)
        ):
            continue
        indices = node.kwargs.get("indices") or node.args[1]

        if len(indices) != 1:
            raise NotImplementedError("We only consider index ops with single index tensor now.")
        index = indices[0]

        if index.meta["tensor_meta"].dtype != torch.int32:
            raise ValueError("We only consider index ops with i32 index tensor now.")


# FIXME: remove `is_quantized_gptj_mlperf_slice_prefill_model` after mlperf.
def _preprocess_gm_for_model_rewrite(
    gm: GraphModule,
    do_decomposition: bool = False,
    is_quantized_gptj_mlperf_slice_prefill_model: bool = False,
    check_for_compilability: bool = True,
) -> None:
    if do_decomposition:
        decompose_linear(gm)
        decompose_layernorm(gm)
    _remove_duplicate_typecasts(gm.graph)
    _remove_unnecessary_larger_typecast_before_index(gm.graph)

    # This is needed for making model slicable by block slicer.
    if is_quantized_gptj_mlperf_slice_prefill_model:
        _make_quantized_gptj_mlperf_slice_prefill_model_slicable(gm)

    if check_for_compilability:
        _check_all_index_ops_i32_index(gm.graph)


def _get_name_from_source(source) -> str:
    if isinstance(source, LocalSource):
        return source.local_name
    elif isinstance(source, GetItemSource):
        return f"{_get_name_from_source(source.base)}_{source.index}"
    else:
        raise NotImplementedError


def _flatten_placeholder_nodes(gm: GraphModule, example_kwargs: Mapping[str, Any]) -> None:
    placeholder_nodes_to_remove = []

    placeholder_nodes = [node for node in gm.graph.nodes if node.op == "placeholder"]

    # Add example value information to placeholder nodes.
    for placeholder_node in placeholder_nodes:
        example_val = example_kwargs[placeholder_node.name]
        placeholder_node.meta["val"] = example_val

    # Make inputs whose type is nested type of tensor to single tensors
    for placeholder_node in placeholder_nodes:
        placeholder_node._dynamo_source = LocalSource(placeholder_node.name)
        example_val = example_kwargs[placeholder_node.name]

        # For inputs with simple type (not list, tuple, ..), we don't need to do anything.
        if isinstance(example_val, (torch.Tensor, float, int, str)):
            placeholder_node.type = type(example_val)
            continue

        nodes_to_search: List[Tuple[Node, Optional[Source]]] = [(placeholder_node, None)]
        new_input_point_nodes_per_source_info: MutableMapping[Source, List[Node]] = defaultdict(
            list
        )

        # BFS while reaching simple tensor node.
        while nodes_to_search:
            node, prev_source_info = nodes_to_search.pop()
            assert isinstance(node, Node)

            if node.op == "placeholder":
                new_source_info: Source = LocalSource(placeholder_node.name)
                val = example_kwargs[placeholder_node.name]
            else:
                assert isinstance(prev_source_info, Source)
                args = map_arg(node.args, lambda n: n.meta["val"])
                kwargs = map_arg(node.kwargs, lambda n: n.meta["val"])
                val = node.target(*args, **kwargs)

                if node.op == "call_function" and node.target == operator.getitem:
                    # Update source info from previous one.
                    new_source_info = GetItemSource(prev_source_info, node.args[1])
                else:
                    assert node.op == "call_function" and isinstance(
                        node.target, torch._ops.OpOverload
                    )
                    continue

            node.meta["val"] = val

            if isinstance(val, (torch.Tensor, int, float)):
                # If current node's value type is tensor, don't search further for this node.
                # This node will become one of inputs (placeholders) of new GraphModule.
                new_input_point_nodes_per_source_info[new_source_info].append(node)
                continue

            # The node value is not tensor. Search further its children.
            for user in node.users:
                nodes_to_search.append((user, new_source_info))

        # Now we got all nodes to be replaced with new input nodes (input point nodes).
        for new_source_info, new_input_nodes in new_input_point_nodes_per_source_info.items():
            # Create new placeholder node that corresponds to `new_source_info`.
            with gm.graph.inserting_after(placeholder_node):
                new_placeholer_node = gm.graph.placeholder(_get_name_from_source(new_source_info))
            new_placeholer_node._dynamo_source = new_source_info
            new_placeholer_node.type = torch.Tensor
            new_placeholer_node.meta["val"] = new_input_nodes[0].meta["val"]

            # Replace existing input point nodes with new placeholder node.
            # Replaced nodes will be removed later through dead code elimination.
            for new_input_node in new_input_nodes:
                new_input_node.replace_all_uses_with(new_placeholer_node)
        placeholder_nodes_to_remove.append(placeholder_node)

    # We don't want setitem nodes to be eliminated by DCE.
    has_side_effect(operator.setitem)
    eliminate_dead_code(gm.graph)

    for placeholder_node in placeholder_nodes_to_remove:
        gm.graph.erase_node(placeholder_node)

    gm.recompile()


def get_aten_gm_from_symbolic_traced_gm(
    gm: GraphModule, example_kwargs: Mapping[str, Any]
) -> GraphModule:
    """Get ATen IR level fx graph from symbolic traced GraphModule (with torch.fx.symbolic_trace).

    Main difference from just calling `make_fx` is that this function generates exactlys same fx graph as calling both `torch._dynamo.export` and `make_fx` to the graph.
    For this, it flattens input/outputs of the graph and adds source information to flattened placeholder nodes.

    """

    # We don't want to affect original gm but share parameter/buffers.
    gm = GraphModule(gm, copy.deepcopy(gm.graph))

    # Flatten input (placeholder noodes) of the graph.
    _flatten_placeholder_nodes(gm, example_kwargs)

    # Lower the graph to ATen IR level.
    flattened_input = flatten_input_tensors(gm, example_kwargs)
    new_gm = make_fx(gm, pre_dispatch=True)(*flattened_input)

    # Copy source info from original graph to lowered graph.
    for torch_ir_gm_ph, aten_gm_ph in zip(gm.graph.nodes, new_gm.graph.nodes):
        if torch_ir_gm_ph.op != "placeholder":
            assert aten_gm_ph.op != "placeholder"
            break
        if hasattr(torch_ir_gm_ph, "_dynamo_source"):
            aten_gm_ph._dynamo_source = torch_ir_gm_ph._dynamo_source

    # Flatten output
    # TODO: Do we need to add info about where each output comes from?
    output_node = next(iter(reversed(new_gm.graph.nodes)))
    assert output_node.op == "output"
    assert len(output_node.args) == 1
    output_node.args = (tree_flatten(output_node.args)[0],)

    # After make_fx, non-tensor placeholders becomes dead nodes but exist. They cannot be removed by `eliminate_dead_code`,
    # so remove them separately.
    for input_element, placeholder_node in zip(flattened_input, new_gm.graph.nodes):
        assert placeholder_node.op == "placeholder"
        if not isinstance(input_element, torch.Tensor):
            new_gm.graph.erase_node(placeholder_node)

    new_gm.recompile()

    return new_gm


def _get_input_layout(t) -> List[Tuple[str, Any]]:
    if isinstance(t, torch.Tensor):
        return [("", "Tensor")]
    elif isinstance(t, (tuple, list)):
        return [
            (f"[{i}]{input_name}", final_elem)
            for i, elem in enumerate(t)
            for input_name, final_elem in _get_input_layout(elem)
        ]
    elif isinstance(t, dict):
        return [
            (f"[{k}]{input_name}", final_elem)
            for k, v in t.items()
            for input_name, final_elem in _get_input_layout(v)
        ]
    elif isinstance(t, (str, int, float)):
        return [("", t)]
    else:
        raise ValueError(f"Unsupported type: {type(t)}")


def trace_model(
    model: torch.nn.Module,
    example_args: Sequence[Any],
    example_kwargs: Mapping[str, Any],
    aten_graph: bool,
    pre_dispatch: bool,
    torch_ir_gm: Optional[GraphModule] = None,
    dynamic_shape: bool = False,
) -> GraphModule:
    flattened_inputs = tree_flatten((example_args, example_kwargs))[0]
    fake_mode = get_fake_mode(chain(model.parameters(), model.buffers(), flattened_inputs))

    # Always trace with fake inputs to avoid real computation.
    fake_args = tree_map_only(torch.Tensor, lambda t: fake_mode.from_tensor(t), example_args)
    fake_kwargs = tree_map_only(torch.Tensor, lambda t: fake_mode.from_tensor(t), example_kwargs)

    if pre_dispatch and not aten_graph:
        raise ValueError("`pre_dispatch` can be True only if `aten_graph` is True.")

    # If torch-IR level GraphModule is given, we don't need to run torch dynamo tracer again.
    if torch_ir_gm and aten_graph:
        if dynamic_shape:
            raise ValueError(
                "Dynamic shape mode is not supported for torch-IR to Aten level GraphModule lowering."
            )
        assert not fake_kwargs
        with enable_python_dispatcher():
            gm = make_fx(torch_ir_gm, pre_dispatch=pre_dispatch)(*fake_args)

        # If `torch_ir_gm` was traced with dynamic shape, unused symbolic ops might remain after make_fx.
        # TODO: There might be other kinds of symbolic ops for other models.
        for node in gm.graph.nodes:
            if node.target == torch.ops.aten.sym_size:
                assert not node.users
                gm.graph.erase_node(node)
    else:
        constraints = []

        torch._dynamo.reset()
        tracing_mode = "symbolic" if dynamic_shape else "static"
        is_prefill = 'past_valid_value_prompt_indices' not in fake_kwargs

        original_model_type = get_original_model_type(model)
        if dynamic_shape:
            if original_model_type in (
                furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
            ):
                # FIXME: This is an optimization just for mlperf.
                for name, value in fake_kwargs.items():
                    if name in ("input_ids", "position_ids", "attention_mask"):
                        if is_prefill:
                            torch._dynamo.mark_dynamic(value, 1)
                    elif name in ("new_key_location", "new_value_location"):
                        if is_prefill:
                            torch._dynamo.mark_dynamic(value, 1)
                    elif name in ("causal_mask",):
                        if is_prefill:
                            torch._dynamo.mark_dynamic(value, 1)
                            torch._dynamo.mark_dynamic(value, 2)
                    elif name.startswith("past_key_values"):
                        for i in range(len(value)):
                            for j in range(len(value[0])):
                                torch._dynamo.mark_dynamic(value[i][j], 0)
            elif original_model_type in (
                furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
                furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
            ):
                # Make attention dim dynamic.
                constraints = [
                    dynamic_dim(fake_kwargs["input_ids"], 1)
                    == dynamic_dim(fake_kwargs["token_type_ids"], 1),
                    dynamic_dim(fake_kwargs["input_ids"], 1)
                    == dynamic_dim(fake_kwargs["position_ids"], 1),
                    dynamic_dim(fake_kwargs["input_ids"], 1)
                    == dynamic_dim(fake_kwargs["attention_mask"], 1),
                ]
                if (
                    original_model_type
                    == furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering
                ):
                    constraints.append(
                        dynamic_dim(fake_kwargs["input_ids"], 1)
                        == dynamic_dim(fake_kwargs["attention_mask"], 2)
                    )

        gm = torch._dynamo.export(
            model,
            aten_graph=aten_graph,
            tracing_mode=tracing_mode,
            same_signature=False,
            pre_dispatch=pre_dispatch,
            constraints=constraints,
        )(*fake_args, **fake_kwargs)[0]

    return gm


def _get_aten_gm(
    fake_model: torch.nn.Module,
    example_args: Sequence,
    example_kwargs: Mapping,
    dynamic_shape_torch_ir_gm_store: Optional[MutableMapping],
    fake_mapping_mode: FakeCopyModeWithMapping,
):
    if isinstance(fake_model, QuantCausalLM):
        if example_args:
            raise NotImplementedError("We don't support fast tracing with example args.")

        # If the model is quantized, torch dynamo tracing is not needed. All we need is just `make_fx`.
        # First convert all positional arguments to keyword arguments.
        example_kwargs_copy = dict(example_kwargs)
        for arg_name, arg in zip(inspect.signature(fake_model).parameters.keys(), example_args):
            example_kwargs_copy[arg_name] = arg

        # Get actual graph module to be run
        is_prefill = fake_model._is_prefill(example_kwargs_copy)
        actual_gm = fake_model.prefill_model if is_prefill else fake_model.decode_model

        logger.info("Generating ATen graph from quantized model with fast tracing.")
        start = time()
        aten_gm = get_aten_gm_from_symbolic_traced_gm(actual_gm, example_kwargs_copy)

        logger.info(f"ATen graph generation and postprocess took {time() - start:.2f} seconds.")
        return aten_gm, aten_gm

    # TODO: add dynamic shape tracing support for other kind of models.
    use_dynamic_shape = get_original_model_type(fake_model) in (
        furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
        furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
        furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
        furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
    )

    if dynamic_shape_torch_ir_gm_store is not None:
        input_info = _get_input_layout((example_args, example_kwargs))
        input_info.sort()
        input_info_hash = get_env_independent_hash(input_info)

        if get_original_model_type(fake_model) in (
            furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
        ):
            is_prefill = 'past_valid_value_prompt_indices' not in example_kwargs
            if is_prefill:
                # For these models, dynamic shape tracing cannnot make batch dimenstion symbolic.
                input_info_hash = get_env_independent_hash(
                    (input_info_hash, example_kwargs["input_ids"].size(0))
                )
        elif get_original_model_type(fake_model) in (
            furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
            furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
        ):
            # For these models, dynamic shape tracing cannnot make batch dimenstion symbolic.
            input_info_hash = get_env_independent_hash(
                (input_info_hash, example_kwargs["input_ids"].size(0))
            )

        if cached := dynamic_shape_torch_ir_gm_store.get(input_info_hash):
            fake_model, torch_ir_gm, fake_mapping_mode = cached
            pass
        else:
            # Trace with ``aten_graph=False`` to find out input tensor order in traced FX graph.
            # Because input name information only remain when ``aten_graph=False``.
            if use_dynamic_shape:
                logger.info("tracing model with dynamic shape")
            else:
                logger.info("tracing model with static shape")

            torch_ir_gm = trace_model(
                fake_model,
                example_args,
                example_kwargs,
                False,
                False,
                dynamic_shape=use_dynamic_shape,
            )
            if use_dynamic_shape:
                dynamic_shape_torch_ir_gm_store[input_info_hash] = (
                    fake_model,
                    torch_ir_gm,
                    fake_mapping_mode,
                )
    else:
        # Trace with ``aten_graph=False`` to find out input tensor order in traced FX graph.
        # Because input name information only remain when ``aten_graph=False``.
        torch_ir_gm = trace_model(
            fake_model, example_args, example_kwargs, False, False, dynamic_shape=use_dynamic_shape
        )

    # Flatten nested type inputs into tuple of tensors.
    # This matching process is not stable. Might work wrong for some inputs.
    # TODO: make this more robust.
    if example_args and example_kwargs:
        raise NotImplementedError("We do not support cases that both args and kwargs exist.")
    inputs = example_args or example_kwargs
    flattened_input = flatten_input_tensors(torch_ir_gm, inputs)

    # If model is Quantized model, trace with pre_dispatch=True. With this,
    # CompositeImplicitAutograd decomposition doesn't occur, and it's the right level
    # that MPPP config is bound to. For example, with CompositeImplicitAutograd decomposition,
    # matmul can be decomposed into bmm or mm with multiple view ops, which makes valid MPPP config
    # fails to propagate because of those flattening view ops.
    #
    # For more details about how matmul op is decomposed by CompositeImplicitAutograd,
    # refer to https://github.com/pytorch/pytorch/blob/6b1f13ea2f3b1bcd575620eecd7d84a4d2e3eb76/torch/_decomp/decompositions.py#L4166
    #
    # TODO: remove this and always trace with `pre_dispatch=True` .
    # For this, mppp configs should be rewritten.
    pre_dispatch = isinstance(fake_model, QuantCausalLM)

    # Get ATen level GraphModule
    aten_gm = trace_model(
        fake_model, flattened_input, {}, True, pre_dispatch, torch_ir_gm=torch_ir_gm
    )

    return torch_ir_gm, aten_gm


def get_aten_graph_with_original_names(
    model: Union[torch.nn.Module, ModelCreationInfo],
    example_args: Sequence,
    example_kwargs: Mapping,
    input_names: Optional[Sequence[str]] = None,
    output_names: Optional[Sequence[str]] = None,
    do_decompositions_for_model_rewrite: bool = False,
    cache_dir: Optional[os.PathLike] = None,
    dynamic_shape_torch_ir_gm_store: Optional[MutableMapping] = None,
) -> Tuple[GraphModule, Tuple[torch.Tensor, ...]]:
    """Get ATen IR level fx graph from model whose nodes have original names.

    Returns:
        Tuple[GraphModule, Tuple[torch.Tensor, ...]]:
            ATen IR level fx graph and input that can be used to run returned GraphModule,
            made by flattening `example_args` and `example_kwargs`.
    """

    # Support GraphModule caching for only ModelMetadata model
    # TODO: add support for normal nn.Module model.
    do_cache = (
        cache_dir is not None and isinstance(model, ModelCreationInfo) and model.is_hashable()
    )
    if isinstance(model, ModelCreationInfo):
        original_type = model.metadata.get_optimized_cls()
        is_quantized = model.metadata.is_quantized
    else:
        original_type = get_original_model_type(model)
        is_quantized = isinstance(model, QuantCausalLM)

    # FIXME: This is hard binded to gptj mlperf slice model.
    is_quantized_gptj_mlperf_slice_prefill_model = (
        original_type is furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM
        and "causal_mask" in example_kwargs
        and is_quantized
    )

    if do_cache:
        assert cache_dir is not None
        gm_path = Path(cache_dir) / "graphmodules"
        gm_path.mkdir(parents=True, exist_ok=True)

        qformat_qparam_path = model.get_qparam_qformat_path()
        pretrained_id = model.metadata.pretrained_id
        model_config = model.metadata.config

        hash_val = get_env_independent_hash(
            (
                TRACER_VERSION,
                hash_model(
                    original_type,
                    model_config,
                    qformat_qparam_path,
                    pretrained_id,
                    model.seed,
                    model.random_weight_model,
                ),
                hash_example_inputs(example_args, example_kwargs),
            )
        )

        quantized_prefix = "Quantized_" if model.metadata.is_quantized else ""
        model_name = f"{quantized_prefix}{original_type.__module__}.{original_type.__name__}"

        cached_gm_file_path = get_cache_path_if_exists(hash_val, "fx", gm_path)

        if cached_gm_file_path:
            # Cached GraphModule exists. Load and return it.
            cached_gm = load_gm(cached_gm_file_path, fill_tensor_meta=True)
            # Flatten nested type inputs into tuple of tensors.
            # This matching process is not stable. Might work wrong for some inputs.
            # TODO: make this more robust.
            if example_args and example_kwargs:
                raise NotImplementedError(
                    "We do not support cases that both args and kwargs exist."
                )
            inputs = example_args or example_kwargs
            flattened_input = flatten_input_tensors(cached_gm, inputs)
            _preprocess_gm_for_model_rewrite(
                cached_gm,
                do_decompositions_for_model_rewrite,
                is_quantized_gptj_mlperf_slice_prefill_model=is_quantized_gptj_mlperf_slice_prefill_model,
            )
            return cached_gm, flattened_input

    # In most cases, output names in FX graph is not meaningful. Therefore, use predefined output names for each model.
    if output_names is None:
        try:
            if isinstance(model, ModelCreationInfo):
                cur_model: Union[torch.nn.Module, ModelMetadata] = model.metadata
            else:
                cur_model = model
            output_names = get_output_names(cur_model)
        except Exception:
            logging.warning(
                "Output tensor names will be obtained from FX graph. This might not be correct."
            )
            pass

    # Instantiate model if it's `ModelCreationInfo` and cache does not exist.
    if isinstance(model, ModelCreationInfo):
        model = model.instantiate_model()

    assert isinstance(model, torch.nn.Module)

    # Copy model to fake model to avoid any real computation or clone.
    flattened_args = tree_flatten(example_args)[0]
    flattened_kwargs = tree_flatten(example_kwargs)[0]
    fake_mode = get_fake_mode(
        chain(model.parameters(), model.buffers(), flattened_args, flattened_kwargs)
    )
    fake_mapping_mode = FakeCopyModeWithMapping(fake_mode)

    # `FakeCopyModeWithMapping` has a mapping from fake tensor to real tensor.
    with fake_mapping_mode:
        fake_model = copy.deepcopy(model)

    gm_with_dynamo_source_info, aten_gm = _get_aten_gm(
        fake_model,
        example_args,
        example_kwargs,
        dynamic_shape_torch_ir_gm_store,
        fake_mapping_mode,
    )

    # Remove aten.sym_size nodes that are created due to dynamic shape tracing.
    for node in aten_gm.graph.nodes:
        if node.op == torch.ops.aten.sym_size:
            assert not node.users
            aten_gm.graph.erase_node(node)

    add_original_name_info(
        fake_model, gm_with_dynamo_source_info, aten_gm, input_names, output_names
    )
    add_qparam_info(fake_model, aten_gm)

    model_parameters = dict(model.named_parameters())
    model_buffers = dict(model.named_buffers())

    # Replace fake tensor constants which have original names and are original model's buffer or parameter with real ones.
    # This is needed because some constant fake tensors are cloned during tracing, which makes `FakeCopyModeWithMapping` impossible to match them.
    for node in aten_gm.graph.nodes:
        if node.op == "get_attr":
            target = getattr(aten_gm, node.target)
            if isinstance(target, FakeTensor):
                if not has_original_name(node):
                    continue
                original_name = get_original_name(node)
                original_tensor_constant: Union[torch.Tensor, torch.nn.Parameter]
                if original_name in model_parameters:
                    original_tensor_constant = model.get_parameter(get_original_name(node))
                elif original_name in model_buffers:
                    original_tensor_constant = model.get_buffer(get_original_name(node))
                else:
                    continue
                assert (
                    target.shape == original_tensor_constant.shape
                    and target.dtype == original_tensor_constant.dtype
                    and target.device == original_tensor_constant.device
                )
                setattr(aten_gm, node.target, original_tensor_constant)

    # Replace remaining fake tensor constants with real ones.
    fake_mapping_mode.set_fake_to_real(True)
    with fake_mapping_mode:
        aten_gm = copy.deepcopy(aten_gm)

    del fake_mapping_mode

    # Fill "tensor_meta" metadata from "example_value" metadata.
    # The result is same as calling ShapeProp, but more efficient.
    fill_tensor_meta_from_val_meta(aten_gm)

    # Save GraphModule to cache dir.
    if do_cache:
        # Copy dynamo_source info from torch ir graph to aten graph.
        for torch_ir_gm_placeholder_node, aten_gm_placeholder_node in zip_equal(
            (node for node in gm_with_dynamo_source_info.graph.nodes if node.op == "placeholder"),
            (node for node in aten_gm.graph.nodes if node.op == "placeholder"),
        ):
            aten_gm_placeholder_node._dynamo_source = torch_ir_gm_placeholder_node._dynamo_source

        # Serialize and save the graphmodule.
        save_gm(
            aten_gm,
            gm_path / f"{model_name}-{hash_val}.fx",
            include_node_metadata=True,
            constant_tensor_path=gm_path / f"{model_name}-tensors-{hash_val}.safetensors",
        )

    _preprocess_gm_for_model_rewrite(
        aten_gm,
        do_decompositions_for_model_rewrite,
        is_quantized_gptj_mlperf_slice_prefill_model=is_quantized_gptj_mlperf_slice_prefill_model,
    )

    # Flatten nested type inputs into tuple of tensors.
    # This matching process is not stable. Might work wrong for some inputs.
    # TODO: make this more robust.
    if example_args and example_kwargs:
        raise NotImplementedError("We do not support cases that both args and kwargs exist.")
    inputs = example_args or example_kwargs
    flattened_input = flatten_input_tensors(gm_with_dynamo_source_info, inputs)

    return aten_gm, flattened_input
