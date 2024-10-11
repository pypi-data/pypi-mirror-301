import contextlib
from functools import partial
from typing import Dict, Iterable, Optional, Sequence, Tuple, Union

import torch
from torch._guards import detect_fake_mode
from torch._ops import OpOverload
from torch._subclasses import FakeTensor, FakeTensorMode
from torch.fx import GraphModule, Node
from torch.fx.passes.shape_prop import ShapeProp, TensorMetadata, _extract_tensor_metadata
from torch.utils._pytree import tree_map_only

from furiosa_llm.parallelize.model_rewriter.mppp_config import DeviceId, ShardSpec

DEVICE_ID_KEY = "device_id"
SPEC_KEY = "spec"


def get_device_id(
    node: Node,
) -> Union[DeviceId, Tuple[DeviceId, ...]]:
    return node.meta[DEVICE_ID_KEY]


def set_device_id(
    node: Node,
    device_id: Union[DeviceId, Tuple[DeviceId, ...]],
):
    node.meta[DEVICE_ID_KEY] = device_id


def has_device_id(node) -> bool:
    return DEVICE_ID_KEY in node.meta


def get_spec(node: Node) -> Union[ShardSpec, Tuple[ShardSpec, ...]]:
    return node.meta[SPEC_KEY]


def set_spec(node: Node, spec: Union[ShardSpec, Tuple[ShardSpec, ...]]):
    node.meta[SPEC_KEY] = spec


def has_spec(node: Node) -> bool:
    return SPEC_KEY in node.meta


def get_fake_mode(tensors: Iterable[torch.Tensor]) -> FakeTensorMode:
    # Get fake mode from ``tensors`` if exist.
    # Otherwise, get currently active one or create new one if there's no currently active one.
    fake_mode_set = set(tensor.fake_mode for tensor in tensors if isinstance(tensor, FakeTensor))
    if len(fake_mode_set) > 1:
        raise ValueError(
            "There must be at most one FakeTensorMode for all parameters, buffers and inputs"
        )
    return (
        fake_mode_set.pop()
        if len(fake_mode_set) == 1
        else detect_fake_mode() or FakeTensorMode(allow_non_fake_inputs=True)
    )


def get_tensor_from_node(
    node: Node, fake_mode: Optional[FakeTensorMode] = None, gm: Optional[GraphModule] = None
) -> torch.Tensor:
    example_val = node.meta.get("val", None)
    if example_val is not None:
        if fake_mode is not None:
            example_val = tree_map_only(torch.Tensor, fake_mode.from_tensor, example_val)
        return example_val

    tensor_meta = node.meta.get("tensor_meta", None)
    if tensor_meta is None:
        if node.op == "get_attr":
            if gm is None:
                raise ValueError(
                    "GraphModule must be provided for get_attr_node with no tensor_meta."
                )
            assert isinstance(node.target, str)
            tensor_meta = _extract_tensor_metadata(getattr(gm, node.target))
        else:
            raise ValueError("`tensor_meta` must be set for the node to get tensor.")
    elif not isinstance(tensor_meta, TensorMetadata):
        raise NotImplementedError("We don't support nested form of tensor_meta now.")
    else:
        pass

    context = fake_mode or contextlib.nullcontext()

    with context:
        # TODO: Is this okay?
        ret = torch.empty(
            tensor_meta.shape,
            dtype=tensor_meta.dtype,
            requires_grad=tensor_meta.requires_grad,
            memory_format=tensor_meta.memory_format,
        ).as_strided(tensor_meta.shape, tensor_meta.stride)
    return ret


def _is_parent_of_lift_fresh_copy(node: Node) -> bool:
    if any(child.target == torch.ops.aten.lift_fresh_copy.default for child in node.users):
        assert len(node.users) == 1
        return True
    return False


def get_real_tensor_from_fake_tensor(fake_tensor: FakeTensor) -> torch.Tensor:
    return torch.zeros(
        fake_tensor.shape,
        dtype=fake_tensor.dtype,
        layout=fake_tensor.layout,
        device=fake_tensor.device,
        requires_grad=fake_tensor.requires_grad,
    )


def add_tensor_meta(node: Node, gm: Optional[GraphModule] = None) -> None:
    assert node.op in ("call_function", "call_module")

    fake_mode = FakeTensorMode(allow_non_fake_inputs=True)
    fake_args = tree_map_only(Node, partial(get_tensor_from_node, fake_mode=fake_mode), node.args)
    fake_kwargs = tree_map_only(
        Node, partial(get_tensor_from_node, fake_mode=fake_mode), node.kwargs
    )

    if node.op == "call_function":
        target = node.target
        assert callable(target)
    elif node.op == "call_module":
        if gm is None:
            raise ValueError("GraphModule must be provided for call_module node.")
        assert isinstance(node.target, str)
        # Get actual module that is callable.
        target = getattr(gm, node.target)

        if isinstance(target, GraphModule):
            # If module is GraphModule, there might be placeholder nodes that is given as the input to `torch.ops.aten.lift_fresh_copy.default` op node,
            # which doesn't allow fake tensor to be an its input. So we need to convert corresponding input tensors that will used as an
            # `torch.ops.aten.lift_fresh_copy.default` op's input back to real tensors.
            placeholder_nodes = tuple(
                node for node in target.graph.nodes if node.op == "placeholder"
            )

            assert len(placeholder_nodes) == len(fake_args)
            fake_args = tuple(
                (
                    get_real_tensor_from_fake_tensor(arg)
                    if _is_parent_of_lift_fresh_copy(placeholder_nodes[i])
                    else arg
                )
                for i, arg in enumerate(fake_args)
            )

            assert len(fake_kwargs) == 0
    else:
        raise ValueError(f"{node.op} node's tensor metadata cannot be derived from other nodes.")

    # Get fake tensor result
    res = target(*fake_args, **fake_kwargs)

    del fake_args, fake_kwargs
    tensor_meta = tree_map_only(torch.Tensor, _extract_tensor_metadata, res)
    node.meta["tensor_meta"] = tensor_meta
    node.meta["val"] = res


def get_normalized_torch_op_node_args(node) -> Tuple[Tuple, Dict]:
    if node.op != "call_function" or not isinstance(node.target, OpOverload):
        raise ValueError("torch op call function node can only be normalized.")
    node_args = list(node.args)
    node_kwargs = dict(node.kwargs)
    for idx, arg in enumerate(node.target._schema.arguments):
        if arg.name not in node_kwargs:
            continue
        if arg.kwarg_only:
            # Remove kwarg whose value is its default value.
            if arg.has_default_value() and arg.default_value == node_kwargs[arg.name]:
                del node_kwargs[arg.name]
                continue
        else:
            # Convert non-kwarg-only kwarg into positional arguments.
            assert idx == len(node_args)
            node_args.append(node_kwargs.pop(arg.name))

    # Remove positional arguments whose value is its default value.
    for i in range(len(node_args) - 1, -1, -1):
        arg_info = node.target._schema.arguments[i]
        if arg_info.has_default_value() and arg_info.default_value == node_args[i]:
            node_args.pop()
        else:
            break

    return tuple(node_args), node_kwargs


def propagate_shape_info_without_real_computation(
    gm: GraphModule, example_args: Sequence[torch.Tensor]
) -> None:
    assert all(isinstance(arg, FakeTensor) for arg in example_args)

    fake_mode = get_fake_mode(example_args)
    fake_example_args = tuple(fake_mode.from_tensor(arg) for arg in example_args)

    original_tensor_constants = {}

    # Replace all tensor constants with fake ones to avoid real computation.
    for node in gm.graph.nodes:
        if node.op != "get_attr" or _is_parent_of_lift_fresh_copy(node):
            continue
        original_tensor_constants[node.target] = getattr(gm, node.target)
        setattr(gm, node.target, fake_mode.from_tensor(original_tensor_constants[node.target]))

    ShapeProp(gm).propagate(*fake_example_args)

    # Restore original tensor constants.
    for attr_name, tensor in original_tensor_constants.items():
        setattr(gm, attr_name, tensor)
    del original_tensor_constants
