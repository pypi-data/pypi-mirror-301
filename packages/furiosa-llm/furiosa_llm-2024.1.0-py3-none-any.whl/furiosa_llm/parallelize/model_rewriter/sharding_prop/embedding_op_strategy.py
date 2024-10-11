# Copyright (c) Meta Platforms, Inc. and affiliates
# implement matrix related ops for distributed tensor
from dataclasses import dataclass, field
import itertools
from typing import Dict, List, Optional, cast

import torch
import torch.distributed._functional_collectives as funcol
from torch.distributed._tensor.op_schema import OpStrategy, PlacementStrategy, StrategyType
from torch.distributed._tensor.ops.utils import is_tensor_shardable
from torch.distributed._tensor.placement_types import (
    DTensorSpec,
    Placement,
    Replicate,
    Shard,
    _Partial,
)
from torch.fx import Node

import furiosa_llm.parallelize.model_rewriter.mppp_config as mrw

aten = torch.ops.aten


@dataclass
class MaskBuffer:
    data: Optional[torch.Tensor] = None

    def materialize_mask(self, mask):
        if self.data is not None:
            raise RuntimeError("MaskBuffer has already been materialized")
        self.data = mask

    def release_mask(self):
        # TODO: evaluate if we need to release the mask buffer or the buffer
        # can just have the same lifetime as the _Partial placement
        if self.data is None:
            raise RuntimeError("MaskBuffer has not been materialized")
        self.data = None

    def apply_mask(self, tensor):
        if self.data is None:
            raise RuntimeError("MaskBuffer has not been materialized")

        # NOTE: _MaskPartial is being used by the embedding op and the gather op.
        # For gather, the mask has the same dimension as the output tensor, whereas
        # the output of the embedding op has an additional dimension compare to the input,
        # hence the output masking logic below having two different cases.
        if tensor.ndim == self.data.ndim:
            tensor[self.data] = 0.0
        else:
            tensor[self.data, :] = 0.0


@dataclass(frozen=True)
class _MaskPartial(_Partial):
    """
    A partial mask placement devised for rowwise sharded embedding op, where we need
    to mask and adjust the indices to the local embedding shard, embedding masking
    is a special type of the Partial placement

    NOTE: the lifecycle of this MaskPartial placement follows the corresponding DTensor
    lifecycle, i.e. the indices_mask would only be alive during the lifetime of the DTensor.
    """

    logical_dim_size: int = -1
    mask_buffer: MaskBuffer = field(default_factory=MaskBuffer)

    def _reduce_value(
        self, tensor: torch.Tensor, mesh: mrw.DeviceMesh, mesh_dim: int
    ) -> torch.Tensor:
        # by the time we ned reduction, we should have already saved the mask
        assert self.mask_buffer.data is not None

        # apply the mask to the tensor that pending reduction
        self.mask_buffer.apply_mask(tensor)

        # clear the mask buffer
        self.mask_buffer.release_mask()

        # perform sum reduction
        return funcol.all_reduce(tensor, reduceOp=self.reduce_op.name, group=(mesh, mesh_dim))  # type: ignore [arg-type]

    def _reduce_shard_value(
        self,
        tensor: torch.Tensor,
        mesh: mrw.DeviceMesh,
        mesh_dim: int,
        shard_spec: Placement,
    ) -> torch.Tensor:
        # by the time we ned reduction, we should have already saved the mask
        assert self.mask_buffer.data is not None

        # apply the mask to the tensor that pending reduction
        self.mask_buffer.apply_mask(tensor)

        # clear the mask buffer
        self.mask_buffer.release_mask()

        # call reduce_shard_tensor of the shard_spec.
        shard_spec = cast(Shard, shard_spec)
        return shard_spec._reduce_shard_tensor(tensor, mesh, self.reduce_op, mesh_dim)  # type: ignore [arg-type]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _MaskPartial):
            return False

        # if either data is not None, we invalidate the sharding cache, as this indicates
        # the current MaskPartial placement is still in use and should not be used for cache hit.
        if self.mask_buffer.data is not None or other.mask_buffer.data is not None:
            return False

        return self.reduce_op == other.reduce_op and self.logical_dim_size == other.logical_dim_size

    def __hash__(self) -> int:
        return 1 + hash((self.logical_dim_size, id(self.mask_buffer.data), self.reduce_op))

    def __repr__(self) -> str:
        """
        machine readable representation of the MaskPartial placement
        """
        return f"_MaskPartial(logical_dim_size={self.logical_dim_size})"

    def __str__(self) -> str:
        """
        human readable representation of the MaskPartial placement
        """
        return "MaskP"


def embedding_strategy(
    node: Node, mesh: mrw.DeviceMesh, node_to_strategy: Dict[Node, StrategyType]
) -> StrategyType:
    """
    This strategy handles embedding op. We have two possible embedding shardings:
    rowwise and colwise
    # TODO: implement rowwise sharding
    """

    weight_strategy = cast(OpStrategy, node_to_strategy[node.all_input_nodes[0]])
    indices_strategy = cast(OpStrategy, node_to_strategy[node.all_input_nodes[1]])

    weight_shape = weight_strategy.strategies[0].output_spec.shape
    indices_shape = indices_strategy.strategies[0].output_spec.shape
    output_emd_dim = len(indices_shape)

    all_mesh_dim_strategies = []

    for mesh_dim in range(mesh.ndim):
        single_mesh_dim_strategies = []

        # placement list stores placements of [output, weight, input_indices]
        # first we always have replicate all for inputs and output
        all_replicate: List[Placement] = [Replicate()] * 3
        single_mesh_dim_strategies.append(all_replicate)

        # colwise sharding, output shard on last dim, weight shard on dim 1, input replicate
        colwise_sharding = [Shard(output_emd_dim), Shard(1), Replicate()]
        single_mesh_dim_strategies.append(colwise_sharding)

        # rowwise sharding, output is embedding partial, weight shard on dim 0, input accepts embedding partial
        embedding_partial_placement = _MaskPartial(logical_dim_size=weight_shape[0])

        # NOTE we want to reuse the same mask partial placement so that we can reuse the same mask that generates
        # from the input indices and use it for output reduction
        rowwise_sharding = [
            embedding_partial_placement,
            Shard(0),
            embedding_partial_placement,
        ]
        single_mesh_dim_strategies.append(rowwise_sharding)

        # batch dim sharding, weight replicated, input can shard on any dim, output follows input
        for input_dim in range(len(indices_shape)):
            batch_sharding = [Shard(input_dim), Replicate(), Shard(input_dim)]
            single_mesh_dim_strategies.append(batch_sharding)

        all_mesh_dim_strategies.append(single_mesh_dim_strategies)

    strategy_combs = itertools.product(*all_mesh_dim_strategies)

    all_strategies = []
    for strategy_comb in strategy_combs:
        spec_list = []
        for specs in zip(*strategy_comb):
            spec_list.append(DTensorSpec(mesh, tuple(specs)))  # type: ignore [arg-type]

        if is_tensor_shardable(weight_shape, spec_list[1]) and is_tensor_shardable(
            indices_shape, spec_list[2]
        ):
            # only add to the strategy list when both weight and indices are shardable
            strat = PlacementStrategy(
                output_spec=spec_list[0],
                input_specs=spec_list[1:],
            )
            all_strategies.append(strat)

    return OpStrategy(all_strategies)
