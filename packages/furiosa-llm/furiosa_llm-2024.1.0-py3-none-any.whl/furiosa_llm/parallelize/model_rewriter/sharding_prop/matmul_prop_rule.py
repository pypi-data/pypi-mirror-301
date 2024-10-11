from typing import Callable

import torch
from torch.distributed._tensor import DTensor
from torch.distributed._tensor.op_schema import OpSchema, OutputSharding
from torch.distributed._tensor.ops.common_rules import einop_rule
from torch.fx.passes.shape_prop import TensorMetadata

import furiosa_llm.parallelize.model_rewriter.mppp_config as mrw
from furiosa_llm.parallelize.model_rewriter.mppp_config import (
    DeviceMesh,
    Partial,
    Placement,
    Replicate,
    Shard,
    ShardSpec,
)

aten = torch.ops.aten


def _prop_dot_product_shard_and_shard(p1: Placement, p2: Placement) -> Placement:
    assert isinstance(p1, Shard)
    assert isinstance(p2, Shard)

    if p1.dim != 0 or p2.dim != 0:
        raise ValueError(f"Vector cannot be sharded in dim {p1.dim}")

    return Partial()


def _prop_dot_product_replicate_and_replicate(p1: Placement, p2: Placement) -> Placement:
    assert isinstance(p1, Replicate)
    assert isinstance(p2, Replicate)

    return Replicate()


def _prop_dot_product_replicate_and_partial(p1: Placement, p2: Placement) -> Placement:
    assert isinstance(p1, Replicate)
    assert isinstance(p2, Partial)

    return Partial()


def _prop_dot_product_partial_and_replicate(p1: Placement, p2: Placement) -> Placement:
    return _prop_dot_product_replicate_and_partial(p2, p1)


def _get_placement_class_name(obj: Placement):
    ret = type(obj).__name__.lower()
    if ret.startswith("_"):
        ret = ret[1:]
    return ret


def matmul_rule(schema: OpSchema) -> OutputSharding:
    """Sharding propgation rule for aten.matmul.default."""
    arg1_spec, arg2_spec = schema.args_spec

    assert isinstance(arg1_spec.tensor_meta, TensorMetadata) and isinstance(
        arg2_spec.tensor_meta, TensorMetadata
    )
    tensor1_shape = arg1_spec.tensor_meta.shape
    tensor2_shape = arg2_spec.tensor_meta.shape
    dim_tensor_1 = len(tensor1_shape)
    dim_tensor_2 = len(tensor2_shape)

    assert isinstance(arg1_spec, mrw.ShardSpec) and isinstance(arg2_spec, mrw.ShardSpec)
    assert arg1_spec.mesh == arg2_spec.mesh

    dev_mesh = arg1_spec.mesh
    assert isinstance(dev_mesh, DeviceMesh)
    arg1_spec.placements

    # totch.aten.matmul works differently according to the shape of the input tensors.
    # For more details, refer to https://pytorch.org/docs/stable/generated/torch.matmul.html
    if dim_tensor_1 == 1 and dim_tensor_2 == 1:
        # dot product
        if dev_mesh.ndim > 1:
            raise NotImplementedError(
                "dot product with larger than 1-dim array devich mesh is not supported now."
            )
        p1, p2 = arg1_spec.placements[0], arg2_spec.placements[0]
        try:
            prop_logic: Callable[[Placement, Placement], Placement] = globals().get(
                f"_prop_dot_product_{_get_placement_class_name(p1)}_and_{_get_placement_class_name(p2)}"  # type: ignore
            )
        except KeyError:
            raise RuntimeError(
                f"Unpropagatable placement combination: {p1} and {p2} for vector product"
            )
        output_placement = prop_logic(p1, p2)
        assert isinstance(output_placement, Placement)

        assert isinstance(arg1_spec.tensor_meta, TensorMetadata)

        tensor_meta = TensorMetadata(
            torch.Size([1]),
            arg1_spec.tensor_meta.dtype,
            arg1_spec.tensor_meta.requires_grad,
            arg1_spec.tensor_meta.stride,
            arg1_spec.tensor_meta.memory_format,
            arg1_spec.tensor_meta.is_quantized,
            arg1_spec.tensor_meta.qparams,
        )

        return OutputSharding(
            ShardSpec(dev_mesh, (output_placement,), tensor_meta),  # type: ignore
        )
    elif dim_tensor_1 == 2 and dim_tensor_2 == 1:
        # matrix-vector product (equals to aten.mv) can be decomposed into aten.mul.Tensor followed by aten.sum.dim_IntList(dim=1)
        op_schema = OpSchema(aten.mul.Tensor._schema, schema.args_schema, schema.kwargs_schema)
        output_sharding = DTensor._propagator.op_to_rules[aten.mul.Tensor](op_schema)

        op_schema = OpSchema(aten.sum.dim_IntList._schema, (output_sharding.output_spec, 1), {})
        return DTensor._propagator.op_to_rules[aten.sum.dim_IntList](op_schema)
    elif dim_tensor_1 == 1 and dim_tensor_2 == 2:
        # matmul between vector and 2d array can be done as ``torch.squeeze(torch.mm(torch.unsqueeze(tensor1, 0), tensor2), 0)``.
        return einop_rule(
            "a,ab->ab",
            schema,
        )
    elif dim_tensor_1 == 2 and dim_tensor_2 == 2:
        # this case is exactly same as aten.mm.default
        schema.func_schema = aten.mm.default._schema
        return DTensor._propagator.op_to_rules[aten.mm.default](schema)
    elif dim_tensor_1 >= 1 and dim_tensor_2 >= 1:

        # batched matrix multiply
        if dim_tensor_1 == 1:
            # prepend 1 to tensor 1 (unsqueeze 0)
            # tensor2's second dim size should be equal to tensor1's first dim size
            alphabets = "cdefghijklmnopqrstuvwxyz"
            tensor2_dims = "ba" + alphabets[: dim_tensor_2 - 2]
            assert tensor1_shape[0] == tensor2_shape[1]

            return einop_rule(
                f"a,{tensor2_dims} -> b{tensor2_dims[2:]}",
                schema,
            )
        elif dim_tensor_2 == 1:
            # append 1 to tensor 2 (unsqueeze -1)
            # tensor 1's final dim width should be eqaul to tensor 2's first dim size
            alphabets = "cdefghijklmnopqrstuvwxyz"
            tensor1_dims = alphabets[: dim_tensor_1 - 1] + "a"
            assert tensor1_shape[-1] == tensor2_shape[0]

            return einop_rule(
                f"{tensor1_dims},a -> {tensor1_dims[:-1]}",
                schema,
            )
        else:
            # Both two matrix's dim is greater than or equal to 2 and at least one of them
            # is greater than 2.
            assert isinstance(arg1_spec.tensor_meta, TensorMetadata) and isinstance(
                arg2_spec.tensor_meta, TensorMetadata
            )
            assert tensor1_shape[-1] == tensor2_shape[-2]

            # all batch dims must be broadcastable
            reversed_arg1_shape = tuple(reversed(tensor1_shape))
            reversed_arg2_shape = tuple(reversed(tensor2_shape))

            for arg1_dim_size, arg2_dim_size in tuple(
                zip(reversed_arg1_shape, reversed_arg2_shape)
            )[2:]:
                assert arg1_dim_size == arg2_dim_size or arg1_dim_size == 1 or arg2_dim_size == 1

            alphabets = "defghijklmnopqrstuvwxyz"

            # Get dims symbol for each tensor. All dimensions except for last two should be broadcastable.
            # That is, either they are eqaul, one of them is 1 or one of them is missing (that dimension exist only for one of them).
            # So represent dim symbols for each tensors with their batch dimensions broadcastable.
            # For example, if dim_tensor1==5 and dim_tensor2 == 4 then tensor1_dims = "fedab" and tensor2_dims = "edbc".
            # Also note that dimension with size 1 can just be represented as same symbol as the other tensor's corresponding dimension.
            tensor1_dims = (
                ''.join(reversed([alphabets[i - 2] for i in range(2, dim_tensor_1)])) + "ab"
            )
            tensor2_dims = (
                ''.join(reversed([alphabets[i - 2] for i in range(2, dim_tensor_2)])) + "bc"
            )

            longest_arg_dims = (
                tensor1_dims if len(tensor1_dims) > len(tensor2_dims) else tensor2_dims
            )

            return einop_rule(
                f"{tensor1_dims},{tensor2_dims}->{longest_arg_dims[:-2]}{tensor1_dims[-2]}{tensor2_dims[-1]}",
                schema,
            )
    else:
        raise ValueError(
            f"Invalid tensor shapes for matmul: {arg1_spec.tensor_meta.shape}, {arg2_spec.tensor_meta.shape}"
        )
