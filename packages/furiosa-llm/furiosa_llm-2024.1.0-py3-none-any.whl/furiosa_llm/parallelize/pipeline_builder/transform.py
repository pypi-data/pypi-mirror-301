from collections import defaultdict
from functools import partial, reduce
import operator
from typing import Any, DefaultDict, Dict, List, MutableMapping, Optional, Sequence, cast

from furiosa_torch_ext.torch_ext import STD_DECOMPOSITIONS, do_make_fx, eliminate_dead_code
import torch
from torch._dynamo.utils import deepcopy_to_fake_tensor
from torch._guards import detect_fake_mode
from torch._subclasses import FakeTensorMode
from torch.fx import Graph, GraphModule, Node
from torch.fx.passes.shape_prop import ShapeProp
from torch.fx.passes.split_module import split_module
from torch.utils._pytree import tree_map_only

from furiosa_llm.models import DecomposedLayerNorm
from furiosa_llm.parallelize.model_rewriter.mppp_config import DeviceId
from furiosa_llm.parallelize.model_rewriter.ops.utils import is_single_dev_comm_op
from furiosa_llm.parallelize.model_rewriter.utils import (
    add_tensor_meta,
    get_device_id,
    get_normalized_torch_op_node_args,
    get_tensor_from_node,
)
from furiosa_llm.parallelize.node_meta import get_color, set_color


# revert shape of parameters to its original shape in fx graph before make_fx.
# NOTE: parameters in GraphModule are transposed in make_fx when it's used by aten.mm.default node.
# I'm not sure this covers all the cases and same problem occurs in other torch versions.
def revert_parameter_shapes_to_before_makefx(gm_after_makefx: GraphModule):
    for node in gm_after_makefx.graph.nodes:
        if node.op != "get_attr":
            continue
        need_transpose = any(str(user.target) == "aten.mm.default" for user in node.users.keys())

        if need_transpose:
            original_constant = getattr(gm_after_makefx, node.name)
            # NOTE: we only consider param with 2 dims
            assert len(original_constant.shape) == 2
            setattr(gm_after_makefx, node.name, original_constant.t())

            with gm_after_makefx.graph.inserting_after(node):
                new_node = gm_after_makefx.graph.create_node(
                    "call_function", torch.ops.aten.transpose.int, (node, 0, 1)
                )

            node.replace_all_uses_with(
                new_node, delete_user_cb=lambda x: x != new_node, propagate_meta=True
            )

    gm_after_makefx.recompile()


def _get_first_call_function_node(graph: Graph) -> Optional[Node]:
    for node in graph.nodes:
        if node.op == "call_function":
            return node
    return None


# is node a submodule that just contains single collective communication?
def _is_replaced_cc(gm: GraphModule, node: Node, submod_prefix: str) -> bool:
    return (
        node.op == "call_module"
        and node.name.startswith(submod_prefix)
        and any(
            is_single_dev_comm_op(node)
            for node in tuple(getattr(gm, cast(str, node.target)).graph.nodes)
        )
    )


def _replicate_nodes_with_multiple_colors(gm: GraphModule) -> None:
    colors_per_dev_id = defaultdict(set)
    to_be_erased = []

    # Find actually assigned colors per device ids.
    for node in gm.graph.nodes:
        if is_single_dev_comm_op(node) or node.op == "output":
            continue
        colors = get_color(node)
        assert isinstance(colors, Sequence)
        if len(colors) == 1:
            dev_id = get_device_id(node)
            assert isinstance(dev_id, DeviceId)
            colors_per_dev_id[dev_id].add(colors[0])

    # Filter out colors that are not assigned to corresponding node's assigned device.
    # This is needed because in the node replication stage, each node's color metadata
    # was copied to the replicated ones.
    for node in gm.graph.nodes:
        if is_single_dev_comm_op(node) or node.op == "output":
            continue
        colors = get_color(node)
        assert isinstance(colors, Sequence)
        dev_id = get_device_id(node)
        assert isinstance(dev_id, DeviceId)

        colors = tuple(color for color in colors if color in colors_per_dev_id[dev_id])
        set_color(node, colors)

    # We need to replicate nodes colored with more than one colors.
    node_to_replicated_node: MutableMapping[Node, Dict[int, Node]] = defaultdict(dict)
    for node in gm.graph.nodes:
        if is_single_dev_comm_op(node) or node.op == "output":
            continue
        colors = get_color(node)
        assert isinstance(colors, Sequence)

        # Don't care about nodes with one color.
        if len(colors) == 1:
            continue

        # Don't need to placeholder, get_attr nodes. These nodes can be shared across partitions.
        if node.op in ("placeholder", "get_attr"):
            for color in colors:
                node_to_replicated_node[node][color] = node
            continue

        dev_id = get_device_id(node)
        assert isinstance(dev_id, DeviceId)

        # Create replica node of the node for each color. Each replica should be connected to the parent node's replica with same color.
        # ASSUMPTION: the node with multiple colors' all parent nodes are all have same colors.
        for color in colors:
            with gm.graph.inserting_before(node):
                new_args = tree_map_only(
                    Node, lambda x: node_to_replicated_node[x][color], node.args
                )
                new_kwargs = tree_map_only(
                    Node, lambda x: node_to_replicated_node[x][color], node.kwargs
                )
                new_node = gm.graph.create_node(node.op, node.target, new_args, new_kwargs)
                new_node.meta = node.meta.copy()
                set_color(new_node, [color])

                node_to_replicated_node[node][color] = new_node

        # Change childs (users) with one color to point to the proper replica node with same color.
        for user in tuple(node.users.keys()):
            user_colors = get_color(user)
            assert isinstance(user_colors, Sequence)
            if len(user_colors) != 1:
                continue
            user_color = user_colors[0]
            user.args = tree_map_only(
                Node,
                lambda x: node_to_replicated_node[x][user_color] if x == node else x,
                user.args,
            )
            user.kwargs = tree_map_only(
                Node,
                lambda x: node_to_replicated_node[x][user_color] if x == node else x,
                user.kwargs,
            )
        to_be_erased.append(node)

    # Erase original node.
    for node in reversed(to_be_erased):
        gm.graph.erase_node(node)


# TODO: refactor this.
def partition_gm(
    gm: GraphModule,
    submod_prefix: str,
    one_supertask_per_device: bool = False,
    use_color_for_partitioning: bool = False,
) -> GraphModule:
    """Transform FX graph into one that is composed of submodules.

    Each submodule is either a collection of computations on same single device or a single collective communication.
    In FX graph, collection of computations are "call_module" node for submodule and collective communication nodes remain same.
    """
    _node_to_partition: DefaultDict[str, Any] = defaultdict(lambda: 1)
    node_to_children: DefaultDict[str, List[str]] = defaultdict(list)
    comm_ops = set()
    partition_cnt = 0
    node_name_to_node = {node.name: node for node in gm.graph.nodes}

    if one_supertask_per_device:
        if use_color_for_partitioning:
            _replicate_nodes_with_multiple_colors(gm)

        def splitter(node):
            if is_single_dev_comm_op(node):
                return node.name
            else:
                color = get_color(node)
                if use_color_for_partitioning:
                    assert isinstance(color, Sequence) and len(color) == 1
                    return f"d{get_device_id(node)}-c{color[0]}"
                else:
                    return f"d{get_device_id(node)}"

        splitted = split_module(gm, None, splitter)
    else:
        if use_color_for_partitioning:
            # TODO
            raise NotImplementedError(
                "Colorwise partitioning without one_supertask_per_device option is not supported yet."
            )
        # calculate node -> its children mapping
        for node in gm.graph.nodes:
            for parent in node.all_input_nodes:
                node_to_children[parent.name].append(node.name)

        to_search = []

        for node in gm.graph.nodes:
            if node.op in ("placeholder", "get_attr", "output"):
                continue
            if node.op == "call_function":
                if not is_single_dev_comm_op(node):
                    continue
                comm_ops.add(node.name)
                _node_to_partition[node.name] = 1 << partition_cnt
                partition_cnt += 1
                for child in node_to_children[node.name]:
                    to_search.append((child, 1 << partition_cnt))

        descendants: Dict[str, List[str]] = {}

        def descendants_of_node(node: str) -> List[str]:
            if node in descendants:
                return descendants[node]
            ret: List[str] = list(
                set(
                    reduce(
                        operator.add,
                        map(lambda n: descendants_of_node(n) + [n], node_to_children[node]),
                        [],
                    )
                )
            )
            descendants[node] = ret
            return ret

        # to prevent reaching recursion limit
        for node in reversed(gm.graph.nodes):
            descendants_of_node(node.name)

        # color each node.
        for node, partition_color in to_search:
            _node_to_partition[node] |= partition_color

            for desc in descendants_of_node(node):
                _node_to_partition[desc] |= partition_color

        for node in gm.graph.nodes:
            if node.name not in _node_to_partition:
                _node_to_partition[node.name] = 0

        for comm_op in comm_ops:
            del _node_to_partition[comm_op]

        for node_name in tuple(_node_to_partition.keys()):
            node = node_name_to_node[node_name]
            if node.op == "output":
                del _node_to_partition[node_name]
                continue
            device_id = get_device_id(node)

            new_partition = (device_id, _node_to_partition[node_name])
            _node_to_partition[node_name] = new_partition

        # normalize partiiotn numbers
        partition_num_normalizer = dict(
            (v, i) for i, v in enumerate(tuple(set(_node_to_partition.values())))
        )

        node_to_partition = dict(
            map(
                lambda kv: (kv[0], partition_num_normalizer[kv[1]]),
                _node_to_partition.items(),
            )
        )

        # maintain name of comm ops
        for i, comm_op in enumerate(comm_ops):
            node_to_partition[comm_op] = comm_op

        for node in gm.graph.nodes:
            if node.op == "get_attr":
                if len(node_to_children[node.name]) == 0:
                    continue
                children_partitions = map(
                    lambda x: node_to_partition[x], node_to_children[node.name]
                )
                node_to_partition[node.name] = next(children_partitions)

        partition_to_node = defaultdict(list)

        for k, v in node_to_partition.items():
            partition_to_node[v].append(k)

        def splitter(node):
            assert node.name in node_to_partition
            return node_to_partition[node.name]

        splitted = split_module(gm, None, splitter)

    output_node_meta = tuple(gm.graph.nodes)[-1].meta.copy()

    for node in tuple(splitted.graph.nodes):
        if _is_replaced_cc(splitted, node, submod_prefix):
            # Replace wrapped cc node which is a call_module node that calls cc insidde with call_function node.
            actual_op_node = _get_first_call_function_node(getattr(splitted, node.name).graph)
            assert actual_op_node is not None
            assert is_single_dev_comm_op(actual_op_node)

            with splitted.graph.inserting_after(node):
                new_node = splitted.graph.call_function(actual_op_node.target)

            new_node.meta = actual_op_node.meta.copy()
            new_node.args = node.args
            node.replace_all_uses_with(new_node)
            splitted.graph.erase_node(node)

    for node in splitted.graph.nodes:
        # If tensor_meta doesn't exist, add it.
        if "tensor_meta" not in node.meta and node.op != "output":
            add_tensor_meta(node, gm=splitted)

    splitted.recompile()

    # restore output node metadata
    tuple(splitted.graph.nodes)[-1].meta = output_node_meta

    # comm ops
    for comm_op in comm_ops:
        assert getattr(splitted, f"{submod_prefix}_{comm_op}") is not None

    return splitted


def convert_to_fake_gm(gm: GraphModule, inputs, fake_mode=None) -> GraphModule:
    """Convert a GraphModule to a GraphModule with fake tensors"""

    if fake_mode is None:
        fake_mode_set = set(map(lambda x: x.fake_mode, inputs))

        assert (
            len(fake_mode_set) == 1
        ), "All the parameters and buffers must have the same FakeTensorMode"

        fake_mode = fake_mode_set.pop() or detect_fake_mode(inputs)

    fake_gm = deepcopy_to_fake_tensor(gm, fake_mode)

    fake_inputs = [fake_mode.from_tensor(t, static_shapes=True) for t in inputs]

    # trace module with fake module
    with fake_mode:
        gm = do_make_fx(fake_gm, fake_inputs, decomposition_table=STD_DECOMPOSITIONS)

    return gm


def decompose_linear(gm: GraphModule) -> None:
    for node in tuple(gm.graph.nodes):
        if not (node.op == "call_function" and node.target == torch.ops.aten.linear.default):
            continue
        with gm.graph.inserting_before(node):
            transpose_node = gm.graph.call_function(torch.ops.aten.t.default, (node.args[1],))
            add_tensor_meta(transpose_node)

            replacement = gm.graph.call_function(
                torch.ops.aten.matmul.default, (node.args[0], transpose_node)
            )
            add_tensor_meta(replacement)

            if len(node.args) == 3:
                replacement = gm.graph.call_function(
                    torch.ops.aten.add.default, (replacement, node.args[2])
                )
                add_tensor_meta(replacement)
        node.replace_all_uses_with(replacement)
        gm.graph.erase_node(node)
    gm.recompile()


def decompose_layernorm(gm: GraphModule):
    fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

    for node in gm.graph.nodes:
        if not (
            node.op == "call_function"
            and node.target
            in (
                torch.ops.aten.native_layer_norm.default,
                torch.ops.aten.layer_norm.default,
            )
        ):
            continue
        node_args, node_kwargs = get_normalized_torch_op_node_args(node)
        node.args = node_args
        node.kwargs = node_kwargs

        # input, normalized_shape, weight , bias, eps when ``torch.ops.aten.native_layer_norm.default``.
        # input, normalized_shape, weight(optional) = 0, bias (optional) = 0, eps (optional) = 1e-5, cudnn_enable (optional) when ``torch.ops.aten.layer_norm.default``.
        # TODO: add support for cases when weight and bias are not given.
        if len(node.args) < 4:
            raise NotImplementedError("We only support layer_norms with weight and bias now.")

        input_, normalized_shape = node.args[:2]
        eps = node.args[4] if len(node.args) > 4 else 1e-5

        sub_gm, _ = torch._dynamo.export(
            DecomposedLayerNorm(normalized_shape, eps=eps),
            aten_graph=True,
            tracing_mode="static",
        )(get_tensor_from_node(input_, fake_mode=fake_mode))

        # To make all get_attr nodes as placeholders.
        splitted = split_module(sub_gm, None, lambda x: 0)
        sub_gm = splitted.submod_0

        subg_placeholders = tuple(node for node in sub_gm.graph.nodes if node.op == "placeholder")
        input_nodes = tuple(arg for arg in node.args if isinstance(arg, Node))

        # fill tensor meta info for nodes in layernorm subgraph.
        ShapeProp(sub_gm).propagate(
            *map(partial(get_tensor_from_node, fake_mode=fake_mode, gm=gm), input_nodes)
        )

        assert len(subg_placeholders) == len(
            input_nodes
        ), f"{len(subg_placeholders)}, {len(input_nodes)}"

        replace_map = {
            subg_placeholder: input_node
            for subg_placeholder, input_node in zip(subg_placeholders, input_nodes)
        }

        with gm.graph.inserting_before(node):
            output_node = gm.graph.graph_copy(sub_gm.graph, replace_map)

        to_be_replaced = []

        if node.target == torch.ops.aten.native_layer_norm.default:
            # aten.native_layer_norm.default produces a tuple of tensors with length 3.
            for user in node.users:
                if (
                    user.op == "call_function"
                    and user.target == operator.getitem
                    and user.args[1] == 0
                ):
                    to_be_replaced.append(user)
                else:
                    if user.users:
                        # Do we need to support this case?
                        raise NotImplementedError(
                            "Pattern using last two output tensors of aten.native_layer_norm cannot be handled now."
                        )
        else:
            # aten.layer_norm.default produces a single tensor
            assert node.target == torch.ops.aten.layer_norm.default
            to_be_replaced.append(node)

        assert isinstance(output_node, Node)

        for original in to_be_replaced:
            original.replace_all_uses_with(output_node)

    eliminate_dead_code(gm.graph)

    gm.recompile()
