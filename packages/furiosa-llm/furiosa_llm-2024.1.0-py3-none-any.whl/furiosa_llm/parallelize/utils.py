from functools import partial, reduce
import json
import operator
import os
import re
import typing
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Type, Union

import torch

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata

import furiosa_llm_models as flm
from safetensors import safe_open
from torch._dynamo.source import AttrSource, GetItemSource, LocalSource
from torch._guards import Source
from torch._ops import OpOverload
from torch.distributed._tensor import DTensor
from torch.fx import GraphModule, Node
from torch.fx.passes.shape_prop import TensorMetadata, _extract_tensor_metadata
from torch.utils._pytree import tree_flatten, tree_map_only
import transformers
from transformers import MODEL_FOR_CAUSAL_LM_MAPPING

from furiosa_llm.parallelize.config import (
    Device,
    DeviceId,
    DeviceMesh,
    MpppConfig,
    Replicate,
    ShardSpec,
)
from furiosa_llm.parallelize.custom_drawer import FuriosaFXGDrawer
from furiosa_llm.parallelize.model_rewriter.utils import get_normalized_torch_op_node_args
from furiosa_llm.parallelize.pipeline.types import ParamfileFormat, Placements
from furiosa_llm.quantized_models import QuantCausalLM

KWARGS_NAME = "kwargs"
aten = torch.ops.aten


def nested_to_dtensor(
    device_mesh,
    placement,
    target,
):
    if isinstance(target, DTensor):
        return target
    elif isinstance(target, torch.Tensor):
        return DTensor.from_local(target, device_mesh, placement)
    elif isinstance(target, List):
        return list(map(partial(nested_to_dtensor, device_mesh, placement), target))
    elif isinstance(target, Tuple):
        return tuple(map(partial(nested_to_dtensor, device_mesh, placement), target))
    else:
        return target


def nested_to_local(target):
    if isinstance(target, DTensor):
        return target.to_local()
    elif isinstance(target, torch.Tensor):
        return target
    elif isinstance(target, List):
        return list(map(nested_to_local, target))
    elif isinstance(target, Tuple):
        return tuple(map(nested_to_local, target))
    else:
        return target


# follow given node's child and return the first DTensor node found.
def get_first_dtensor_descendant(node: Node, allow_multiple_children=False) -> Node:
    while not isinstance(node.meta["example_value"], DTensor):
        assert allow_multiple_children or len(node.users) == 1
        child = tuple(node.users.keys())[0]
        node = child
    return node


# follow given node's child and return the first DTensor node found.
def get_first_dtensor_ancestor(node: Node) -> Node:
    while not isinstance(node.meta["example_value"], DTensor):
        assert len(node.all_input_nodes) == 1 and node.target == "to_local"
        node = node.all_input_nodes[0]
    return node


def draw_graph(gm, name: str = "", mppp_config: Optional[MpppConfig] = None):
    """
    Draw the given graph and save it to a file if DUMP_SVG_TO environment variable is set.
    """
    from time import localtime, strftime

    save_dir = os.environ.get("DUMP_SVG_TO", None)
    if save_dir is None:
        return

    os.makedirs(save_dir, exist_ok=True)
    name += f'_{strftime("%H%M%S", localtime())}'
    svg_path = os.path.join(save_dir, f"{name}.svg")
    drawer = FuriosaFXGDrawer(gm, name)
    dot = drawer.get_dot_graph()

    if mppp_config is None:
        dot.write_svg(svg_path)
        return

    for static_id in mppp_config.static_tensors.keys():
        n = dot.get_node(static_id)
        if not n:
            continue
        n = n[0]
        n.set_color("blue")
        n.set_penwidth("3")
        n.set_style("filled, diagonals")
    dynamic_tensors = {(dspec.src, dspec.dst): dspec.spec for dspec in mppp_config.dynamic_tensors}

    for (src, dst), spec in dynamic_tensors.items():
        e = dot.get_edge(src, dst)
        if len(e) != 1:
            print(RuntimeError(f"Edge {src} -> {dst} not found"))
            continue
        e = e[0]
        e.set_label(spec._to_brief_str())
        e.set_color("blue")
        e.set_penwidth("3")
    dot.write_svg(svg_path)


def _get_original_name(source: Source) -> str:
    if isinstance(source, GetItemSource):
        return _get_original_name(source.base)
    elif isinstance(source, LocalSource):
        return source.local_name
    elif isinstance(source, AttrSource):
        return f"{_get_original_name(source.base)}.{source.member}"
    else:
        raise ValueError(f"Unknown source type: {source}")


def _get_tensor(obj, source: Source):
    if isinstance(source, GetItemSource):
        return _get_tensor(obj, source.base)[source.index]
    elif isinstance(source, LocalSource):
        if source.local_name not in obj and source.local_name == KWARGS_NAME:
            assert isinstance(obj, dict)
            return obj
        else:
            return obj[source.local_name]
    elif isinstance(source, AttrSource):
        return getattr(_get_tensor(obj, source.base), source.member)
    else:
        raise NotImplementedError(f"Unsuported source: {source}")


def flatten_input_tensors(
    torch_ir_gm: GraphModule, original_inputs: Union[Sequence, Mapping]
) -> Tuple:
    if isinstance(original_inputs, Sequence):
        return tuple(
            reduce(
                operator.add,
                (flatten_input_tensors(torch_ir_gm, input_) for input_ in original_inputs),
                (),
            )
        )
    elif isinstance(original_inputs, Mapping):
        placeholder_nodes = tuple(
            node for node in torch_ir_gm.graph.nodes if node.op == "placeholder"
        )

        args_in_order = tuple(
            _get_tensor(original_inputs, node._dynamo_source)
            for node in placeholder_nodes
            if hasattr(node, "_dynamo_source")
        )
        return args_in_order
    else:
        if isinstance(original_inputs, torch.Tensor):
            return (original_inputs,)
        else:
            return ()


def get_torch_major_version() -> str:
    # e.g., "2.1"
    return ".".join(torch.__version__.split(".", 2)[0:2])


def is_aten_op(func: Callable) -> bool:
    return isinstance(func, OpOverload) and func._schema.name.startswith("aten")


def is_custom_op(func: Callable) -> bool:
    return isinstance(func, OpOverload) and func._schema.name.startswith("furiosa::")


def gen_mppp_config_with_no_parallelism(
    name: str, model: GraphModule, device: Device
) -> MpppConfig:
    device_id = DeviceId("0")
    static_tensors = {
        node.name: ShardSpec([Replicate()], DeviceMesh([device_id]))
        for node in model.graph.nodes
        if not node.all_input_nodes
    }

    return MpppConfig(
        name=name,
        devices={device_id: device},
        static_tensors=static_tensors,
        dynamic_tensors=[],
    )


def get_output_names(model: Union["ModelMetadata", torch.nn.Module]) -> List[str]:
    # FIXME: directly compare using isinstance
    if hasattr(model, "get_optimized_cls"):
        # model is ModelMetadata
        is_quantized = model.is_quantized
        model_class = model.get_optimized_cls()
    else:
        assert isinstance(model, torch.nn.Module)
        is_quantized = isinstance(model, QuantCausalLM)
        model_class = get_original_model_type(model)

    if model_class == transformers.LlamaForCausalLM:
        output_names = ["logits"]
        for layer_idx in range(model.config.num_hidden_layers):
            for kv_idx in range(2):
                output_names.append(f"past_key_values_{layer_idx}_{kv_idx}")
        # Original Llama's FX graph produces hidden states as its output.
        # TODO: let traced fx graph not produce hidden_states.
        output_names.append("hidden_states")
        return output_names
    elif model_class == MODEL_FOR_CAUSAL_LM_MAPPING[model.config.__class__] or model_class in (
        flm.gptj.symbolic.huggingface.GPTJForCausalLM,
        flm.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
        flm.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
    ):
        # original huggingface PretrainedModel.
        output_names = ["logits"]
        for layer_idx in range(model.config.num_hidden_layers):
            for kv_idx in range(2):
                output_names.append(f"past_key_values_{layer_idx}_{kv_idx}")
        return output_names
    elif model_class in (
        transformers.BertForQuestionAnswering,
        transformers.RobertaForQuestionAnswering,
    ):
        return ["start_logits", "end_logits"]
    elif model_class in (
        flm.gptj.symbolic.preallocated_concat.GPTJForCausalLM,
        flm.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
    ):
        output_names = ["logits"]
        for kv_idx in range(2):
            for layer_idx in range(model.config.num_hidden_layers):
                output_names.append(f"past_key_values_{layer_idx}_{kv_idx}")
        return output_names
    elif model_class in (
        flm.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
        flm.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
        flm.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
        flm.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
        flm.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
        flm.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
    ):
        return ["logits"]
    elif model_class in (
        flm.llama.symbolic.mlperf_submission.LlamaForCausalLM,
        flm.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM,
        flm.llama3.symbolic.mlperf_submission.LlamaForCausalLM,
        flm.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM,
    ):
        # Number of outputs are different depending on whether the model is quantized or not.
        # Why..?
        if is_quantized:
            return ["logits"]
        else:
            return ["logits", "hidden_states"]
    else:
        raise NotImplementedError(f"Cannot get output names for model {model_class}")


def load_partial_param(
    param_file_path: Union[os.PathLike, str],
    tensor_name: str,
    placements: Placements,
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
    *,
    cache: Dict[Any, Any],
    device: str = "cpu",
) -> torch.Tensor:
    if format == format.__class__.SAFETENSORS:
        try:
            f = cache[param_file_path, device]
        except KeyError:
            f = cache[param_file_path, device] = safe_open(
                param_file_path, framework="pt", device=device
            )
        # If tensor is a shared tensor and not stored, get stored one.
        if metadata := f.metadata():
            tensor_name = metadata.get(tensor_name, tensor_name)
        if not placements:
            # if tensor is scalar value with 0 dim.
            tensor = f.get_tensor(tensor_name)
            if tensor.dim() > 0:
                raise ValueError(
                    f"tensor {tensor_name} is not scalar even if its placements is empty"
                )
            return tensor
        tensor_slice = f.get_slice(tensor_name)
        return tensor_slice[[slice(*p) for p in placements]]
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


# Is 10 iterations sufficient?
_WL_ITERATION = 10


def _get_only_needed_tensor_meta_for_hashing(node: Node, gm: GraphModule) -> Tuple:
    example_val = node.meta.get("val")
    tensor_meta = node.meta.get("tensor_meta")
    if example_val is not None:
        tensor_meta = _extract_tensor_metadata(example_val)
    elif tensor_meta is not None:
        pass
    elif node.op == "get_attr":
        assert isinstance(node.target, str)
        example_val = getattr(gm, node.target)
        tensor_meta = _extract_tensor_metadata(example_val)
    else:
        raise ValueError(
            "There's no way to get tensor meta from node. Fill 'val' or 'tensor_meta'."
        )

    # We don't care about other information such as memory_format, requires_grad, and quantization metadata.
    return tree_map_only(TensorMetadata, lambda x: (x.shape, x.dtype, x.stride), tensor_meta)


def hash_fx_graph(gm: GraphModule) -> str:
    import networkx as nx  # type: ignore[import-untyped]

    g = nx.DiGraph()
    placeholder_cnt = 0

    type_emulation_in_out: Set
    try:
        type_emulation_in_out = {
            torch.ops.furiosa.type_emulation_in.default,
            torch.ops.furiosa.type_emulation_out.default,
        }
    except ImportError:
        type_emulation_in_out = set()

    INFO_ATTR = "label"
    SPECIAL_MARKER_FOR_NODE = "special_marker_for_node_@#$$!##"

    for node in gm.graph.nodes:
        edges = []
        attrs = {"op": node.op}
        if node.op == "placeholder":
            attrs["idx"] = placeholder_cnt
            attrs["tensor_meta"] = _get_only_needed_tensor_meta_for_hashing(node, gm)
            placeholder_cnt += 1
        elif node.op == "get_attr":
            attrs["tensor_meta"] = _get_only_needed_tensor_meta_for_hashing(node, gm)
        elif node.op == "call_function":
            attrs["target"] = str(node.target)

            node_args = tuple(node.args)
            node_kwargs = dict(node.kwargs)

            if isinstance(node.target, OpOverload):
                node_args, node_kwargs = get_normalized_torch_op_node_args(node)

            # We don't consider Node in kwargs now. It's very rare case.
            flattened_kwargs, _ = tree_flatten(node_kwargs)
            assert all(not isinstance(x, Node) for x in flattened_kwargs)

            # type_emulation_in/out op's third argument is node's name, we don't want it to be used for hashing.
            if node.target in type_emulation_in_out:
                node_args = node_args[:2] + node_args[3:]

            node_replaced_args = tree_map_only(Node, lambda x: SPECIAL_MARKER_FOR_NODE, node_args)
            node_replaced_kwargs = tree_map_only(
                Node, lambda x: SPECIAL_MARKER_FOR_NODE, node_kwargs
            )

            attrs["args"] = node_replaced_args
            attrs["kwargs"] = node_replaced_kwargs

            # We don't consider Node in kwargs now. It's very rare case.
            flattened_kwargs, _ = tree_flatten(node_replaced_kwargs)
            assert all(not isinstance(x, Node) for x in flattened_kwargs)

            flattened_args, _ = tree_flatten(node_args)
            for i, arg in enumerate(flattened_args):
                if not isinstance(arg, Node):
                    continue
                edges.append((arg.name, node.name, {INFO_ATTR: i}))
        elif node.op == "call_module":
            # We only consider fx graph with no call_module node now (e.g., aten-level fx graph).
            raise NotImplementedError("Fx grpah containing call module node is not supported yet.")
        elif node.op == "output":
            assert len(node.kwargs) == 0
            node_replaced_args = tree_map_only(Node, lambda x: SPECIAL_MARKER_FOR_NODE, node.args)
            attrs["args"] = node_replaced_args

            flattened_args, _ = tree_flatten(node.args)
            for i, arg in enumerate(flattened_args):
                if not isinstance(arg, Node):
                    continue
                edges.append((arg.name, node.name, {INFO_ATTR: i}))
        else:
            raise NotImplementedError(node)

        class Encoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (torch.dtype, torch.device)):
                    return str(obj)
                elif isinstance(obj, (torch.memory_format, torch.layout)):
                    return ""
                else:
                    return super().default(obj)

        label = json.dumps(attrs, indent=2, sort_keys=True, cls=Encoder)
        node_attr = {INFO_ATTR: label}
        g.add_node(node.name, **node_attr)
        for src, dst, attrs in edges:
            g.add_edge(src, dst, **attrs)

    return nx.weisfeiler_lehman_graph_hash(
        g, node_attr=INFO_ATTR, edge_attr=INFO_ATTR, iterations=_WL_ITERATION
    )


def get_original_model_type(model: torch.nn.Module) -> Type:
    if isinstance(model, QuantCausalLM):
        return model.original_type
    else:
        return model.__class__


_KV_CACHE_PATTERN = r"past_key_values_[0-9]+_[0-9]+"


def is_kvcache(name: str) -> bool:
    return re.compile(_KV_CACHE_PATTERN).match(name) is not None


def check_gms_strict_equal(gm1: GraphModule, gm2: GraphModule) -> bool:
    """Check two gms are strictly equal, including node order, names, and actual tensor constant values."""
    if len(gm1.graph.nodes) != len(gm2.graph.nodes):
        return False

    node1_node_to_idx = {node.name: i for i, node in enumerate(gm1.graph.nodes)}
    node2_node_to_idx = {node.name: i for i, node in enumerate(gm2.graph.nodes)}

    for node1, node2 in zip(gm1.graph.nodes, gm2.graph.nodes):
        if node1.op != node2.op or node1.target != node2.target:
            return False
        if node1.op == "get_attr":
            if not getattr(gm1, node1.target).equal(getattr(gm2, node2.target)):
                return False
        for attr_name in ("args", "kwargs"):
            node1_list, node1_spec = tree_flatten(getattr(node1, attr_name))
            node2_list, node2_spec = tree_flatten(getattr(node2, attr_name))
            if len(node1_list) != len(node2_list):
                return False
            if node1_spec != node2_spec:
                return False
            for arg1, arg2 in zip(node1_list, node2_list):
                if isinstance(arg1, Node):
                    if not isinstance(arg2, Node):
                        return False
                    if node1_node_to_idx[arg1.name] != node2_node_to_idx[arg2.name]:
                        return False
                if isinstance(arg1, torch.Tensor):
                    if not isinstance(arg2, torch.Tensor):
                        return False
                    if not arg1.equal(arg2):
                        return False
                else:
                    if arg1 != arg2:
                        return False
    return True


def is_typecast_node(node: Node) -> bool:
    # TODO: add more ops
    if node.op == "call_function":
        if node.target == aten.to.dtype:
            return True
        elif node.target == aten._to_copy.default:
            assert isinstance(node.target, OpOverload)
            mutable_kwargs_copy = dict(node.kwargs)
            for arg in node.target._schema.arguments:
                if not arg.has_default_value():
                    continue
                # Delete default kwargs.
                # Default value can be None or False.
                if arg.name in node.kwargs and arg.default_value == node.kwargs[arg.name]:
                    del mutable_kwargs_copy[arg.name]
            return tuple(mutable_kwargs_copy) == ("dtype",)
        else:
            return False
    return False
