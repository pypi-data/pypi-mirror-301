from itertools import chain
import logging
import operator
from typing import Any, Dict, Iterable, List, Tuple, Union, cast

import torch
from torch._ops import OpOverload
from torch.distributed._tensor import DTensor
from torch.distributed._tensor.op_schema import (
    OpStrategy,
    OutputSharding,
    PlacementStrategy,
    StrategyType,
)
from torch.distributed._tensor.placement_types import DTensorSpec
from torch.fx import GraphModule, Node
from torch.fx.experimental.proxy_tensor import get_isolated_graphmodule
from torch.fx.interpreter import Interpreter
from torch.fx.passes.shape_prop import _extract_tensor_metadata
from torch.utils._pytree import tree_flatten, tree_unflatten

import furiosa_llm.parallelize.model_rewriter.mppp_config as mrw
from furiosa_llm.parallelize.model_rewriter.mppp_config import MpppConfig, Placement, Shard
from furiosa_llm.parallelize.model_rewriter.sharding_prop.embedding_op_strategy import (
    embedding_strategy,
)
from furiosa_llm.parallelize.model_rewriter.sharding_prop.matmul_prop_rule import matmul_rule
from furiosa_llm.parallelize.model_rewriter.sharding_prop.prop_rules import (
    flatten_rule,
    repeat_interleave_rule,
)
from furiosa_llm.parallelize.model_rewriter.utils import get_spec, has_spec, set_spec

aten = torch.ops.aten
logger = logging.getLogger(__name__)


class OpSchema(torch.distributed._tensor.op_schema.OpSchema):
    """
    This class is a wrapper around torch.distributed._tensor.op_schema.OpSchema
    to provide a clean list of args spec list consits of either torch's ShardSpec
    or furiosa_llm's ShardSpec.
    """

    @property
    def args_spec(self) -> Tuple[Union[DTensorSpec, mrw.ShardSpec], ...]:
        """
        args_spec: Tuple[ShardSpec, ...]: contains a clean list of args spec list
            with NO non-DTensor positional arguments (i.e. int/float/tuple, etc)
            mainly used by sharding propagation to propagate the output spec
        """
        # filter out non-relevant values from args schema to get a clean spec list
        # this would mainly be used by sharding propagation rules
        return tuple(
            item for item in self.args_schema if isinstance(item, (DTensorSpec, mrw.ShardSpec))
        )


def _prepare_op_graph(
    op_overload: OpOverload,
    op_schema: OpSchema,
) -> GraphModule:
    from torch._subclasses import FakeTensorMode

    # prepare the op graph for sharding propagation
    # special case op list, we don't need to propagate for local
    # scalar. TODO: figure out a better way to handle this
    skip_prop_list = [
        aten._local_scalar_dense.default,
        aten.equal.default,
        aten.is_same_size.default,
    ]
    if op_overload in skip_prop_list:
        raise RuntimeError(f"error preparing op_graph, {op_overload} is in skip_prop_list")

    # NOTE: We must call the tracing in fake tensor mode so that it
    # avoids materializing memory
    with FakeTensorMode():
        fake_args = op_schema.gen_fake_args()
        fake_kwargs = op_schema.gen_fake_kwargs()
        g = get_isolated_graphmodule(op_overload, fake_args, fake_kwargs)

    return g


def identity_rule(schema: OpSchema) -> OutputSharding:
    return OutputSharding(schema.args_spec)


class ShardingPropagator(Interpreter):
    op_to_rules = DTensor._propagator.op_to_rules
    op_strategy_funcs = DTensor._propagator.op_strategy_funcs

    def __init__(
        self,
        module: GraphModule,
        mppp_config: MpppConfig,
        garbage_collect_values: bool = True,
    ):
        super().__init__(module, garbage_collect_values)
        self.static_tensors = mppp_config.static_tensors
        self.dynamic_tensors = {
            (dspec.src, dspec.dst): dspec.spec for dspec in mppp_config.dynamic_tensors
        }

        # Use updated embedding strategy for aten.embedding
        # FIXME: should update only once (for now the code is written in idempotent manner)
        self.op_to_rules.pop(aten.embedding.default, None)

        # ``aten.divide`` is alias for ``aten.div``. We do this because there's no rule for aten.divide.
        # https://github.com/pytorch/pytorch/blob/6b1f13ea2f3b1bcd575620eecd7d84a4d2e3eb76/aten/src/ATen/native/BinaryOps.cpp#L907
        self.op_to_rules.update({aten.divide.Tensor: self.op_to_rules[aten.div.Tensor]})
        self.op_to_rules.update(
            {torch.ops.furiosa.sparse_select.default: self.op_to_rules[aten.index.Tensor]}
        )

        # add rules for furiosa custom ops
        try:
            # to register custom ops.
            import model_compressor.nn.custom_ops  # type: ignore # noqa: F401

            self.op_to_rules.update(
                {
                    torch.ops.furiosa.away_from_zero_fp2fxp.default: self.op_to_rules[
                        aten.round.default
                    ]
                }
            )
            self.op_to_rules.update({torch.ops.furiosa.type_emulation_in.default: identity_rule})
            self.op_to_rules.update({torch.ops.furiosa.type_emulation_out.default: identity_rule})
        except ImportError:
            pass

        self.op_strategy_funcs.update({aten.embedding.default: embedding_strategy})
        self.op_to_rules.update({aten.matmul.default: matmul_rule})
        self.op_to_rules.update({aten.repeat_interleave.self_int: repeat_interleave_rule})
        self.op_to_rules.update({aten.flatten.using_ints: flatten_rule})
        self.op_to_rules.update({aten.dropout.default: identity_rule})

        node_to_index: Dict[Node, int] = {}
        for idx, node in enumerate(self.module.graph.nodes):
            node_to_index[node] = idx
            if has_spec(node):
                raise ValueError(f"Node {node.name} already has spec before sharding propagation.")
        self.node_to_index = node_to_index

    def get_spec(self, src: Node, dst: Node) -> mrw.ShardSpec:
        """get spec of ``src``, when it's used by ``dst``."""
        if spec := self.dynamic_tensors.get((src.name, dst.name)):
            return spec
        else:
            spec_ = get_spec(src)
            assert isinstance(spec_, mrw.ShardSpec)
            return spec_

    def has_spec(self, src: Node, dst: Node) -> bool:
        """check if ``src`` has spec when it's used by ``dst``."""
        return (src.name, dst.name) in self.dynamic_tensors or has_spec(src)

    def _get_arg_schema_and_placements(
        self,
        node: Node,
        flat_args_list: List[Any],
    ) -> Tuple[
        List[Union[Any, mrw.ShardSpec]],
        List[Tuple[str, mrw.ShardSpec]],
    ]:
        flat_args_schema: List[Union[Any, mrw.ShardSpec]] = []
        placements: List[Tuple[str, mrw.ShardSpec]] = []
        for arg in flat_args_list:
            if isinstance(arg, Node):
                if not self.has_spec(arg, node):
                    raise RuntimeError(
                        f"{arg.name} node doesn't have tensor distribution spec in the graph"
                    )
                placement_spec = self.get_spec(arg, node)
                placement_spec.tensor_meta = arg.meta.get("tensor_meta")

                if arg.op == "get_attr" and not placement_spec.tensor_meta:
                    placement_spec.tensor_meta = _extract_tensor_metadata(
                        getattr(self.module, arg.target)
                    )

                placements.append((arg.name, placement_spec))
                flat_args_schema.append(placement_spec)
            else:
                flat_args_schema.append(arg)
        return flat_args_schema, placements

    def run_node(self, node: Node) -> Any:
        total_nodes = len(self.node_to_index) - 1
        node_idx = self.node_to_index[node]
        logger.debug(
            f"\n{'='*20} running {node_idx}/{total_nodes}"
            f"({(node_idx / total_nodes) * 100:.2f}%) {node.name} {'='*20}"
        )

        if node.op == "output":
            output_node_args = cast(Iterable[Node], node.args[0])
            set_spec(node, tuple(self.get_spec(arg, node) for arg in output_node_args))
            return

        env_args, env_kwargs = self.fetch_args_kwargs_from_env(node)

        val = node.meta.get(
            "val", getattr(self.module, node.target) if node.op == "get_attr" else None  # type: ignore [arg-type]
        )
        assert val is not None, f"can't find node {node.name} in module"
        logger.debug(f"node.name: {node.name}, val: {val}, args: {env_args}, kwargs: {env_kwargs}")

        if has_spec(node):
            return val

        if node.op == "call_function":
            flat_args_list, args_spec = tree_flatten(node.args)
            flat_kwargs_list, kwargs_spec = tree_flatten(node.kwargs)
            placements = []

            if node.target == operator.getitem:
                assert len(flat_args_list) == 2 and len(flat_kwargs_list) == 0
                assert isinstance(flat_args_list[0], Node) and isinstance(flat_args_list[1], int)
                arg_node, idx = flat_args_list

                spec = self.get_spec(arg_node, node)
                if isinstance(spec, (tuple, list)):
                    spec = spec[idx]
                set_spec(node, spec)
                return val

            flat_args_schema, args_placements = self._get_arg_schema_and_placements(
                node, flat_args_list
            )
            placements.extend(args_placements)
            flat_kwargs_schema, kwargs_placements = self._get_arg_schema_and_placements(
                node, flat_kwargs_list
            )
            placements.extend(kwargs_placements)

            op_overload = cast(OpOverload, node.target)

            # check all input tensors' ShardSpec have same device mesh.
            device_mesh = None

            def _assert_same_dev_mesh(arg):
                nonlocal device_mesh
                if isinstance(arg, DTensorSpec):
                    if device_mesh is None:
                        device_mesh = arg.mesh
                    elif device_mesh != arg.mesh:
                        err_msg = f"this op receives tensors with more than one device mesh: {device_mesh}, {arg.mesh}"
                        node.meta["prop_error_msg"] = err_msg
                        raise RuntimeError(err_msg)
                elif isinstance(arg, (list, tuple)):
                    for a in arg:
                        _assert_same_dev_mesh(a)

            _assert_same_dev_mesh(chain(flat_args_schema, flat_kwargs_schema))

            logger.debug(
                "op {} in strategy_funcs {} / in rules {}".format(
                    op_overload.__name__,
                    op_overload in self.op_strategy_funcs,
                    op_overload in self.op_to_rules,
                )
            )

            a = tree_unflatten(flat_args_schema, args_spec)
            k = tree_unflatten(flat_kwargs_schema, kwargs_spec)

            a = list(a)
            k = dict(k)

            # This is needed because many propagation rules cannot handle arguments with kwargs. Remove those as much as possible.
            for idx, arg in enumerate(op_overload._schema.arguments):
                if arg.name not in k:
                    continue
                if arg.kwarg_only:
                    # Remove kwarg whose value is its default value.
                    if arg.has_default_value() and arg.default_value == k[arg.name]:
                        del k[arg.name]
                        continue
                else:
                    # Convert non-kwarg-only kwarg into positional arguments.
                    assert idx == len(a)
                    a.append(k.pop(arg.name))
            a = tuple(a)

            op_schema = OpSchema(op_overload._schema, a, k)

            if op_overload in self.op_to_rules:
                if node.target == torch.ops.furiosa.sparse_select.default:
                    # Remove args spec for arguments we added, to reuse propagation rule for aten.index.Tensor.
                    op_schema.args_schema = op_schema.args_schema[0:2]

                sharding_prop_func = self.op_to_rules[op_overload]
                logger.debug(f"overload: {op_overload} args: {a} kwargs{k}")
                logger.debug(op_schema.args_spec)
                output_shardings = sharding_prop_func(op_schema)
                if output_shardings.output_spec is None:
                    logger.critical(f"output_shardings: {output_shardings}")
                    logger.critical(f"args: {a} kwargs: {k}")
                    logger.critical(f"op_overload: {op_overload} op_schema: {op_schema}")
                    prop_error_msg = f"op_overload={op_overload}\nop_schema={op_schema}\noutput_shardings={output_shardings}"
                    node.meta["prop_error_msg"] = prop_error_msg.replace('<', '&lt;').replace(
                        '>', '&gt;'
                    )
                    raise RuntimeError("Output spec cannot be derived from input specs")

                if isinstance(output_shardings.output_spec, (list, tuple)):
                    # assert all the output specs are the same
                    assert all(
                        spec == output_shardings.output_spec[0]
                        for spec in output_shardings.output_spec
                    ), f"output specs are not the same: {output_shardings.output_spec}"
                    output_spec = output_shardings.output_spec[0]
                else:
                    output_spec = output_shardings.output_spec

                output_spec: mrw.ShardSpec = mrw.ShardSpec(  # type: ignore [no-redef]
                    output_spec.mesh,
                    output_spec.placements,
                    output_spec.tensor_meta,
                )

                set_spec(node, output_spec)
                return val
            elif op_overload in self.op_strategy_funcs:
                op_gm = _prepare_op_graph(op_overload, op_schema)
                # generate op strategy for the op, this is done by propagating
                # the sharding in the graph.
                flat_args_sharding, _ = tree_flatten(
                    [op_schema.args_schema, op_schema.kwargs_schema]
                )
                node_to_strategy: Dict[Node, StrategyType] = {}
                out_node_strategy = None
                mesh = flat_args_sharding[0].mesh
                placeholder_idx = 0
                for n in op_gm.graph.nodes:
                    if n.op == "placeholder":
                        # set sharding to placeholders if it's Node
                        if isinstance(flat_args_sharding[placeholder_idx], DTensorSpec):
                            strategy = PlacementStrategy(flat_args_sharding[placeholder_idx])
                            # for eager execution, inputs only have one fixed sharding
                            node_to_strategy[n] = OpStrategy([strategy])
                        placeholder_idx += 1
                    elif n.op == "call_function":
                        if isinstance(n.target, OpOverload):
                            op_strategy_func = self.op_strategy_funcs[op_overload]
                            out_strategies = op_strategy_func(n, mesh, node_to_strategy)
                            node_to_strategy[n] = out_strategies
                        else:
                            raise NotImplementedError(f"Unsupported function: {n.target}")
                    elif n.op == "output":
                        output_node = n.args[0]
                        out_node_strategy = node_to_strategy[output_node[0]]
                    else:
                        raise NotImplementedError(f"Unsupported node type: {n.op}")

                # NOTE: This had the assumption we only have one call_function op in the
                # op graph, we need to harden this logic when there're decomposed ops.
                assert isinstance(out_node_strategy, OpStrategy)

                # Find strategy that can propagate current input arg specs
                # without redistribution.
                logger.debug(f"out_strategies: {out_strategies}")
                for output_strategy in out_node_strategy.strategies:
                    needs_redistribute = False
                    expected_input_specs = []
                    for idx, input_spec in enumerate(op_schema.args_spec):
                        desired_spec = (
                            output_strategy.output_spec
                            if output_strategy.input_specs is None
                            else output_strategy.input_specs[idx]
                        )
                        expected_input_specs.append(desired_spec)

                        if input_spec != desired_spec:
                            needs_redistribute = True
                            break

                    if not needs_redistribute:
                        break

                if needs_redistribute:
                    node.meta["prop_error_msg"] = (
                        f"Cannot find appropriate propagation rule for op {op_overload} with input arg spec {op_schema.args_spec}"
                    )
                    raise RuntimeError(
                        f"Cannot find appropriate propagation rule for op {op_overload} with input arg spec {op_schema.args_spec}"
                    )

                set_spec(
                    node,
                    mrw.ShardSpec(
                        output_strategy.output_spec.mesh,
                        output_strategy.output_spec.placements,
                        node.meta.get("tensor_meta", None),
                    ),
                )
                return val
            else:
                just_specs: List[mrw.ShardSpec] = [p[1] for p in placements]

                try:
                    p = placements.pop()
                except IndexError:
                    raise ValueError(
                        f"Node {node.name} has no parents, but its spec is not given by mppp config."
                    ) from None

                def to_positive_idx(idx: int, total: int) -> int:
                    return idx if idx >= 0 else total + idx

                if op_overload in (
                    torch.ops.aten.gather.default,
                    torch.ops.furiosa.gather_i32.default,
                ):
                    if op_overload == torch.ops.aten.gather.default:
                        # gather receives 3 args in order: (input (tensor), dim (int), index(tensor))
                        # gather can be propagated only if input and index have same ShardSpec and not be sharded in ``dim`` dimension.
                        assert len(node.args) == 3 and len(just_specs) == 2
                    elif op_overload == torch.ops.furiosa.gather_i32.default:
                        assert len(node.args) in (3, 4) and len(just_specs) == 2
                    input_spec, index_spec = just_specs

                    gather_dim = node.args[1]
                    assert isinstance(gather_dim, int)
                    assert isinstance(input_spec, DTensorSpec) and isinstance(
                        index_spec, DTensorSpec
                    )
                    assert input_spec.tensor_meta is not None

                    input_tensor_num_dim = len(input_spec.tensor_meta.shape)

                    if input_spec.placements != index_spec.placements:
                        err = (
                            f"input and index should have same placements, "
                            f"but got {input_spec.placements} and {index_spec.placements}"
                        )
                        node.meta["prop_error_msg"] = err
                        raise RuntimeError(err)

                    sharded_dims = set(
                        to_positive_idx(cast(Shard, plac).dim, input_tensor_num_dim)
                        for plac in input_spec.placements
                        if plac.is_shard()
                    )
                    if to_positive_idx(gather_dim, input_tensor_num_dim) in sharded_dims:
                        raise ValueError(
                            "ShardingPropagationError: aten.gather's input tensors should not be sharded in gather_dim"
                        )

                    set_spec(node, input_spec)
                elif op_overload == torch.ops.aten.stack.default:
                    # stack receives 2 args in order: (inputs (list of tensors), dim (int))
                    # stack can be propagated only if all input tensors have same DTensorProp.
                    if len(node.args) == 1:
                        gather_dim = node.kwargs["dim"]
                    elif len(node.args) == 2:
                        gather_dim = node.args[1]
                    else:
                        assert False

                    assert isinstance(node.args[0], (tuple, list)) and len(just_specs) == len(
                        node.args[0]
                    )
                    assert isinstance(gather_dim, int)
                    input_tensor_spec = just_specs[0]
                    assert all(
                        spec.placements == input_tensor_spec.placements for spec in just_specs
                    )
                    assert input_tensor_spec.tensor_meta is not None

                    input_tensor_num_dim = len(input_tensor_spec.tensor_meta.shape)
                    gather_dim = to_positive_idx(gather_dim, input_tensor_num_dim)

                    # create new ShardSpec with sharded_dim increased by 1 if sharded_dim >= gather_dim
                    new_placements: List[Placement] = []
                    for placement in input_tensor_spec.placements:
                        if placement.is_shard():
                            sharded_dim = to_positive_idx(
                                cast(Shard, placement).dim, input_tensor_num_dim
                            )
                            new_placement = (
                                Shard(sharded_dim + 1) if sharded_dim >= gather_dim else placement
                            )
                        else:
                            new_placement = placement  # type: ignore [no-redef]
                        new_placements.append(new_placement)
                    set_spec(node, mrw.ShardSpec(input_tensor_spec.mesh, tuple(new_placements)))  # type: ignore [arg-type]
                else:

                    def assert_all_replicated(specs):
                        nonlocal device_mesh
                        if isinstance(specs, (list, tuple)):
                            for spec in specs:
                                assert_all_replicated(spec)
                        elif isinstance(specs, DTensorSpec):
                            if not all(p.is_replicate() for p in specs.placements):
                                node.meta["prop_error_msg"] = (
                                    f"Cannot find appropriate propagation rule for op {op_overload} with input arg spec {op_schema.args_spec}"
                                )
                                raise RuntimeError(
                                    f"Cannot find appropriate propagation rule for op {op_overload} with input arg spec {op_schema.args_spec} "
                                    f"Device mesh: {device_mesh}, specs: {specs}"
                                )
                        else:
                            raise ValueError(f"Invalid type object {specs}")

                    assert_all_replicated(just_specs)
                    logger.debug(
                        f"no sharding prop func for {op_overload}, propagating {p[0]} (one of {p[1]}) as is"
                    )
                    set_spec(node, p[1])
                    return val

        return val

    def propagate(self) -> None:
        # Make node_name to node map
        node_name_to_node: Dict[str, Node] = {node.name: node for node in self.module.graph.nodes}

        for node_name, spec in self.static_tensors.items():
            try:
                node = node_name_to_node[node_name]
            except KeyError:
                raise KeyError(f"invalid mppp config, can't find static tensor named {node_name}")
            set_spec(node, spec)

        for (src, dst), spec in self.dynamic_tensors.items():
            for node_id in (src, dst):
                if node_id not in node_name_to_node:
                    raise ValueError(f"invalid mppp config, can't find node named {node_id}")
            node = node_name_to_node[src]

            if dst not in map(lambda x: x.name, node.users):
                raise ValueError(
                    f"invalid mppp config, can't find dynamic tensor {src} -> {dst} (users={node.users.keys()})"
                )
            # # Do we need to handle the case that does not satisfy this condition?
            # assert node not in self.nodes_with_dynamic_spec, "two dynamic spec exist for same node"
            # self.nodes_with_dynamic_spec[node] = spec

        super().run()
