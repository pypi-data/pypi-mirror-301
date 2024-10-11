from typing import List, cast

import torch
from torch.distributed._tensor.op_schema import OpSchema, OutputSharding
from torch.distributed._tensor.placement_types import DTensorSpec
from torch.fx.passes.shape_prop import TensorMetadata

from furiosa_llm.parallelize.model_rewriter.mppp_config import (
    Partial,
    Placement,
    Replicate,
    Shard,
    ShardSpec,
)

aten = torch.ops.aten


def flatten_rule(schema: OpSchema) -> OutputSharding:
    """propagation rule for aten.flatten.using_ints."""
    if len(schema.args_schema) == 1:
        input_ = schema.args_schema[0]
        assert isinstance(input_, DTensorSpec)
        start_dim = 0
        end_dim = -1
    elif len(schema.args_schema) == 2:
        input_, start_dim = schema.args_schema  # type: ignore
        assert isinstance(start_dim, int)
        end_dim = -1
    elif len(schema.args_schema) == 3:
        input_, start_dim, end_dim = schema.args_schema  # type: ignore
        assert isinstance(start_dim, int)
        assert isinstance(end_dim, int)
    else:
        assert False, f"flatten_rule: unexpected number of args: {len(schema.args_schema)}"

    assert isinstance(input_, DTensorSpec) and isinstance(input_.tensor_meta, TensorMetadata)
    # make start, end_dim index positive
    start_dim = start_dim + len(input_.tensor_meta.shape) if start_dim < 0 else start_dim
    end_dim = end_dim + len(input_.tensor_meta.shape) if start_dim < 0 else start_dim

    # original dimension -> dimension after flattened.
    dim_map = {}
    for i in range(len(input_.tensor_meta.shape)):
        if i < start_dim:
            dim_map[i] = i
        elif i <= end_dim:
            dim_map[i] = start_dim
        else:
            dim_map[i] = i - (end_dim - start_dim)

    new_placements: List[Placement] = []

    for placement in input_.placements:
        # Other placements except for Shard can be propagated as is.
        if isinstance(placement, (Partial, Replicate)):
            new_placements.append(placement)
            continue

        assert isinstance(placement, Shard)
        # only need to handle shard cases
        # can be propagated only if sharded dimension is not one of flattened dimensions or is first dimension among flattened ones.
        if placement.dim < start_dim or placement.dim > end_dim:
            new_shard = Shard(dim_map[placement.dim])
        elif placement.dim == start_dim:
            new_shard = Shard(start_dim)
        else:
            raise ValueError(
                f"flatten_rule: dim {placement.dim} is out of range [{start_dim}, {end_dim}]"
            )
        new_placements.append(new_shard)

    return OutputSharding(ShardSpec(input_.mesh, tuple(new_placements)))


def repeat_interleave_rule(schema: OpSchema) -> OutputSharding:
    """propagation rule for aten.repeat_interleave.self_int"""
    if len(schema.args_schema) == 2:
        input_spec, repeats = schema.args_schema
        dim = schema.kwargs_schema["dim"]
    elif len(schema.args_schema) == 3:
        input_spec, repeats, dim = schema.args_schema
    assert isinstance(input_spec, DTensorSpec)

    # If input is sharded into ``dim``, this cannot be propagatable.
    if any(
        placement.is_shard() and cast(Shard, placement).dim == dim
        for placement in input_spec.placements
    ):
        raise ValueError("torch.ops.aten.repeat_interleave cannot be propagated")

    return OutputSharding(input_spec)
