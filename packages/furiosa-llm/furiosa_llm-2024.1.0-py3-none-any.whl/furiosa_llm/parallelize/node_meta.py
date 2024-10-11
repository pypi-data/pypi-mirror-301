import enum
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from pydantic import BaseModel
import torch
from torch.fx import GraphModule, Node
from torch.fx.passes.shape_prop import TensorMetadata, _extract_tensor_metadata
from torch.utils._pytree import tree_map_only

_ORIGINAL_NAME_FIELD_NAME = "original_name"
_UNSHARDED_TENSOR_META_FIELD_NAME = "unsharded_shape"
_CONSTANT_EMBEDDING_POLICY_FIELD_NAME = "constant_embedding_policy"
_QPARAM_KIND_FIELD_NAME = "qparam_kind"
_COLOR_FIELD_NAME = "color"
_GM_HASH_FIELD_NAME = "gm_hash"
_IS_WEIGHT_PARAM_FIELD_NAME = "is_weight_param"


class ConstantEmbeddingPolicy(enum.Enum):
    SHOULD_BE_EMBEDDED = enum.auto()
    SHOULD_BE_INPUT = enum.auto()


def set_original_name(node: Node, original_name: Union[str, Tuple[str, ...]]):
    node.meta[_ORIGINAL_NAME_FIELD_NAME] = original_name


def get_original_name(node: Node) -> str:
    return node.meta[_ORIGINAL_NAME_FIELD_NAME]


def has_original_name(node: Node) -> bool:
    return _ORIGINAL_NAME_FIELD_NAME in node.meta


def get_unsharded_tensor_meta(node: Node) -> Union[TensorMetadata, Sequence[TensorMetadata]]:
    return node.meta[_UNSHARDED_TENSOR_META_FIELD_NAME]


def set_unsharded_tensor_meta(
    node: Node, tensor_meta: Union[TensorMetadata, Sequence[TensorMetadata]]
) -> None:
    node.meta[_UNSHARDED_TENSOR_META_FIELD_NAME] = tensor_meta


def set_to_be_embedded(node: Node):
    if node.op != "get_attr":
        raise ValueError("Only get_attr nodes can have constant embedding metadata.")
    node.meta[_CONSTANT_EMBEDDING_POLICY_FIELD_NAME] = ConstantEmbeddingPolicy.SHOULD_BE_EMBEDDED


def set_to_be_input(node: Node):
    if node.op != "get_attr":
        raise ValueError("Only get_attr nodes can have constant embedding metadata.")
    node.meta[_CONSTANT_EMBEDDING_POLICY_FIELD_NAME] = ConstantEmbeddingPolicy.SHOULD_BE_INPUT


def should_be_embedded(node: Node) -> bool:
    if node.op != "get_attr":
        raise ValueError("Only get_attr nodes can have constant embedding metadata.")
    return (
        node.meta.get(_CONSTANT_EMBEDDING_POLICY_FIELD_NAME, None)
        == ConstantEmbeddingPolicy.SHOULD_BE_EMBEDDED
    )


def should_be_input(node: Node) -> bool:
    if node.op != "get_attr":
        raise ValueError("Only get_attr nodes can have constant embedding metadata.")
    return (
        node.meta.get(_CONSTANT_EMBEDDING_POLICY_FIELD_NAME, None)
        == ConstantEmbeddingPolicy.SHOULD_BE_INPUT
    )


def get_color(node: Node) -> Optional[Tuple[int, ...]]:
    return node.meta.get(_COLOR_FIELD_NAME, None)


def set_color(node: Node, color: Sequence[int]) -> None:
    node.meta[_COLOR_FIELD_NAME] = tuple(color)


class QParamKind(str, enum.Enum):
    SCALE = enum.auto()
    ZERO_POINT = enum.auto()
    # zero-points for operations running on DPE. These qparams must go through emulation_in operator before being used for any other operations.
    ZERO_POINT_FOR_DPE = enum.auto()


def set_qparam_kind(node, qparam_kind: QParamKind):
    node.meta[_QPARAM_KIND_FIELD_NAME] = qparam_kind


def get_qparam_kind(node) -> Optional[QParamKind]:
    return node.meta.get(_QPARAM_KIND_FIELD_NAME, None)


def is_qparam(node: Node) -> bool:
    return _QPARAM_KIND_FIELD_NAME in node.meta


def set_gm_hash(node: Node, hash: str) -> None:
    node.meta[_GM_HASH_FIELD_NAME] = hash


def get_gm_hash(node: Node) -> Optional[str]:
    return node.meta.get(_GM_HASH_FIELD_NAME)


def set_as_weight_param(node: Node) -> None:
    node.meta[_IS_WEIGHT_PARAM_FIELD_NAME] = True


def is_weight_param(node: Node) -> bool:
    return node.meta.get(_IS_WEIGHT_PARAM_FIELD_NAME, False)


class SerializableMetadata(BaseModel):
    original_name: Optional[Union[str, Tuple[str, ...]]] = None
    qparam_kind: Optional[QParamKind] = None
    is_weight_param: Optional[bool] = None

    @classmethod
    def from_node(cls, node: Node):
        return cls(
            original_name=get_original_name(node) if has_original_name(node) else None,
            qparam_kind=get_qparam_kind(node),
            is_weight_param=is_weight_param(node),
        )


def serialize_metadata(node: Node) -> str:
    metadata = SerializableMetadata.from_node(node)
    return metadata.model_dump_json(exclude_none=True)


def deserialize_metadata(value: str) -> Dict[str, Any]:
    metadata = SerializableMetadata.model_validate_json(value)
    return metadata.model_dump(exclude_none=True)


def fill_tensor_meta_from_val_meta(gm: GraphModule) -> None:
    # Generate "tensor_meta" metadata from "val" metadata which contains example value for corresponding node.
    # The result is same as calling ShapeProp, but more efficient.
    for node in gm.graph.nodes:
        if node.op == "get_attr":
            node.meta["tensor_meta"] = _extract_tensor_metadata(getattr(gm, node.target))
        elif node.op == "output":
            continue
        else:
            node.meta["tensor_meta"] = tree_map_only(
                torch.Tensor, _extract_tensor_metadata, node.meta["val"]
            )
