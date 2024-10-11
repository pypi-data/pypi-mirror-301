import base64
import dataclasses
import json
import logging
import os
from pathlib import Path
import typing
from typing import MutableMapping, Optional, Union

from safetensors import safe_open
import torch
from torch._dynamo.utils import deepcopy_to_fake_tensor
from torch._export.serde.schema import Graph
from torch._export.serde.serialize import (
    EnumEncoder,
    GraphModuleDeserializer,
    GraphModuleSerializer,
    _dict_to_dataclass,
)
from torch._subclasses.fake_tensor import FakeTensor, FakeTensorMode
from torch.fx import Node

from furiosa_llm.parallelize.node_meta import (
    deserialize_metadata,
    fill_tensor_meta_from_val_meta,
    serialize_metadata,
)
from furiosa_llm.parallelize.pipeline_builder.utils import write_without_concurrency_issue
from furiosa_llm.parallelize.utils import get_torch_major_version
from furiosa_llm.utils import zip_equal

try:
    # 2.2
    from torch.export.graph_signature import ExportGraphSignature  # type: ignore
except ModuleNotFoundError:
    # 2.1
    from torch._export.exported_program import CallSpec, ExportGraphSignature  # type: ignore

from torch._dynamo.source import AttrSource, GetItemSource, LocalSource
from torch._guards import Source
from torch.fx import GraphModule
from torch.fx.experimental import symbolic_shapes

_NODE_META_KEY = "node_metas"
_DYNAMO_SOURCE_KEY = "dynamo_source"
_NODE_NAMES_KEY = "node_names"
_CONSTANT_TENSOR_PATH_KEY = "constant_tensor_path"
_ATTR_NODE_ORIGINAL_TARGET_INFO_KEY = "attr_node_original_target_info"

_SUPPORTED_DYNAMO_SOURCE_TYPES = {LocalSource, GetItemSource, AttrSource}


def _dynamo_source_dict_to_class(cls, data):
    """dict_to_class converter for torch._guards.Source type."""
    if cls is typing.Any:
        return data
    elif issubclass(cls, Source):
        for candidate_cls in _SUPPORTED_DYNAMO_SOURCE_TYPES:
            try:
                obj = candidate_cls(**data)
                type_hints = typing.get_type_hints(candidate_cls)
                for f in dataclasses.fields(candidate_cls):
                    name = f.name
                    new_field_obj = _dynamo_source_dict_to_class(
                        type_hints[name], getattr(obj, name)
                    )
                    data[name] = new_field_obj
                # because candidate class can be frozen class.
                return candidate_cls(**data)
            except Exception:
                pass
        assert False
    elif isinstance(data, (str, int, bool)):
        assert not issubclass(cls, Source)
        return data
    else:
        assert False


def _check_supported_dynamo_source(obj: Source) -> None:
    if isinstance(obj, LocalSource):
        pass
    elif isinstance(obj, GetItemSource):
        if not isinstance(obj.index, (int, str)):
            raise NotImplementedError("Int or str type indexing is allowed now")
        if obj.index_is_slice:
            raise NotImplementedError("Slice indexing is not supported")
        _check_supported_dynamo_source(obj.base)
    elif isinstance(obj, AttrSource):
        _check_supported_dynamo_source(obj.base)
    else:
        raise NotImplementedError(f"Unsupported source type: {type(obj)}")


def _add_metadata(gm: GraphModule, dict_: MutableMapping) -> None:
    # Some node names can be changed during serialization. So save original names.
    node_names = [node.name for node in gm.graph.nodes]
    dict_[_NODE_NAMES_KEY] = node_names

    # Store some metadata for each node because those metadata is lost during serialization.
    node_metas = {}
    for node in gm.graph.nodes:
        assert node.name not in node_metas
        node_metas[node.name] = serialize_metadata(node)
    assert _NODE_META_KEY not in dict_
    dict_[_NODE_META_KEY] = node_metas

    # Store _dynamo_source info for each node if exists.
    # This informration is used for matching graph placeholder nodes to original input tenosrs.
    dynamo_source_info = {}
    for node in gm.graph.nodes:
        if node.op != "placeholder":
            break
        if source := getattr(node, "_dynamo_source", None):
            _check_supported_dynamo_source(source)
            assert isinstance(source, Source)
            dynamo_source_info[node.name] = dataclasses.asdict(source)

    if dynamo_source_info:
        dict_[_DYNAMO_SOURCE_KEY] = dynamo_source_info


def _save_constants_in_gm(gm: GraphModule, path: Path) -> GraphModule:
    # Save constant tensors to separate file and replace parameters/buffers in model with dummy tensor.
    # Why don't just remove those tensors from the model? Because it makes get_attr nodes invalid and this cause problem during serialization.
    constants = {
        node.target: getattr(gm, node.target) for node in gm.graph.nodes if node.op == "get_attr"
    }

    fake_mode = FakeTensorMode()
    fake_gm = deepcopy_to_fake_tensor(gm, fake_mode)

    # `_dynamo_source` field is not copeid with deepcopy. Copy manually.
    for fake_node, node in zip_equal(fake_gm.graph.nodes, gm.graph.nodes):
        if source_info := getattr(node, "_dynamo_source", None):
            fake_node._dynamo_source = source_info

    DUMMY_TENSOR = torch.tensor(
        0,
        dtype=torch.float32,
        requires_grad=False,
        device="cpu",
    )

    for node in fake_gm.graph.nodes:
        if node.op != "get_attr":
            continue
        original_constant = constants[node.target]
        if isinstance(original_constant, torch.nn.Parameter):
            setattr(
                fake_gm,
                node.target,
                torch.nn.Parameter(DUMMY_TENSOR),
            )
        else:
            setattr(fake_gm, node.target, DUMMY_TENSOR)
        assert not isinstance(getattr(fake_gm, node.target), FakeTensor)

    # Save tensor constants to `constant_tensor_path`.
    write_without_concurrency_issue(
        constants,
        path,
    )
    return fake_gm


def _check_gm_and_get_serializer(gm: GraphModule) -> GraphModuleSerializer:
    constant_not_scalar = False
    for node in gm.graph.nodes:
        if node.op != "get_attr":
            continue
        actual_tensor = getattr(gm, node.target)
        assert not isinstance(
            actual_tensor, FakeTensor
        ), "``GraphModule`` containing ``FakeTensor`` cannot be serialized"
        if len(actual_tensor.size()) > 0:
            # If constant is not a scalar tensor.
            constant_not_scalar = True
    if constant_not_scalar:
        logging.warning(
            "Tensor with size will be included in serialized graph. Serialized graph size might be large."
        )

    torch_version = get_torch_major_version()
    if torch_version == "2.1":
        serializer = GraphModuleSerializer(
            ExportGraphSignature([], [], [], [], {}, {}, {}, None), CallSpec(None, None), []  # type: ignore
        )
    elif torch_version == "2.2":
        serializer = GraphModuleSerializer(ExportGraphSignature([], []), [])  # type: ignore
    else:
        raise NotImplementedError(f"Unsupported torch version: {torch_version}")
    return serializer


def serialize_gm(
    gm: GraphModule,
    include_node_metadata: bool = False,
) -> str:
    serializer = _check_gm_and_get_serializer(gm)
    serialized_graph = serializer.serialize_graph(gm)

    dict_ = dataclasses.asdict(serialized_graph)

    if include_node_metadata:
        _add_metadata(gm, dict_)

    ser_json = json.dumps(dict_, cls=EnumEncoder)

    return base64.b64encode(ser_json.encode("utf-8")).decode("utf-8")


def save_gm(
    gm: GraphModule,
    path: Path,
    include_node_metadata: bool = False,
    constant_tensor_path: Optional[Path] = None,
) -> None:
    serializer = _check_gm_and_get_serializer(gm)

    # If `constant_tensor_path` is not None, save constant tensors to separate file and replace parameters/buffers in model with dummy tensor.
    if constant_tensor_path is not None:
        gm = _save_constants_in_gm(gm, constant_tensor_path)

    # convert gm into dictinary.
    serialized_graph = serializer.serialize_graph(gm)
    dict_ = dataclasses.asdict(serialized_graph)

    # Add information about constant file path.
    if constant_tensor_path is not None:
        dict_[_CONSTANT_TENSOR_PATH_KEY] = str(constant_tensor_path.absolute())

    # During serialization, tensor constants referenced by get_attr nodes saved by get_attr nodes' names, not by its target.
    # That is, if there's multiple get_attr nodes referencing same tensor, multiple copies of that tensor are saved and restored,
    # with each get_attr nodes' having different target name.
    # To restore this kind of copies after loading gm, we save each get_attr node's original target info.
    attr_node_original_target = {}
    for node in gm.graph.nodes:
        if node.op != "get_attr":
            continue
        attr_node_original_target[node.name] = node.target
    dict_[_ATTR_NODE_ORIGINAL_TARGET_INFO_KEY] = attr_node_original_target

    if include_node_metadata:
        _add_metadata(gm, dict_)

    ser_json = json.dumps(dict_, cls=EnumEncoder)
    serialized = base64.b64encode(ser_json.encode("utf-8")).decode("utf-8")
    write_without_concurrency_issue(serialized, path)


def load_gm(
    path: Union[str, os.PathLike],
    fill_tensor_meta: bool,
) -> GraphModule:
    with open(path, "r") as f:
        return deserialize_gm(f.read(), fill_tensor_meta=fill_tensor_meta)


def deserialize_gm(json_program: str, fill_tensor_meta: bool = True) -> GraphModule:
    json_program = base64.decodebytes(json_program.encode("utf-8")).decode("utf-8")
    graph = json.loads(json_program)

    node_metas = graph.pop(_NODE_META_KEY, None)
    dynamo_source_info = graph.pop(_DYNAMO_SOURCE_KEY, None)
    node_names = graph.pop(_NODE_NAMES_KEY, None)
    constant_tensor_path = graph.pop(_CONSTANT_TENSOR_PATH_KEY, None)
    attr_node_original_target = graph.pop(_ATTR_NODE_ORIGINAL_TARGET_INFO_KEY, None)

    serialized_graph = _dict_to_dataclass(Graph, graph)
    assert isinstance(serialized_graph, Graph)

    gm_serializer = GraphModuleDeserializer()
    gm_serializer.shape_env = symbolic_shapes.ShapeEnv(assume_static_by_default=True)

    torch_version = get_torch_major_version()
    if torch_version == "2.1":
        fake_tensor_mode = FakeTensorMode(shape_env=gm_serializer.shape_env)  # type: ignore
    elif torch_version == "2.2":
        fake_tensor_mode = FakeTensorMode(
            shape_env=gm_serializer.shape_env, static_shapes=True  # type: ignore
        )
    else:
        raise NotImplementedError(f"Unsupported torch version: {torch_version}")

    gm_serializer.fake_tensor_mode = fake_tensor_mode
    gm_serializer.symbol_name_to_symbol = {}
    gm_serializer.symbol_name_to_range = {}

    gm_serializer.deserialize_graph(serialized_graph)

    # Update node names if information exists.
    if node_names:
        for node, original_name in zip_equal(gm_serializer.graph.nodes, node_names):
            assert isinstance(node, Node)
            node.name = original_name

    # Update metadata if serialized node metadata exists.
    if node_metas:
        for node in gm_serializer.graph.nodes:
            node.meta.update(deserialize_metadata(node_metas[node.name]))

    # If constant tensor path exists, load constant tensors from the file and replace dummy parameter/buffers of the model with them.
    if constant_tensor_path is not None:
        with safe_open(constant_tensor_path, framework="pt", device="cpu") as f:  # type: ignore[attr-defined]
            for tensor_name in f.keys():
                val = f.get_tensor(tensor_name)
                # NOTE: Information about whether the constant was buffer or parameter is gone here. Is this okay..?
                delattr(gm_serializer.module, tensor_name)
                setattr(gm_serializer.module, tensor_name, val)

    # Restore original target names of get_attr nodes and copies of same tensor constants.
    # For details, see `save_gm` function.
    if attr_node_original_target is not None:
        for node in gm_serializer.graph.nodes:
            if node.op != "get_attr":
                continue
            original_target = attr_node_original_target[node.name]
            if original_target != node.target:
                delattr(gm_serializer.module, node.target)
            node.target = original_target

    # Update _dynamo_source info if exists
    if dynamo_source_info:
        num_placeholders = len(
            [node for node in gm_serializer.graph.nodes if node.op == "placeholder"]
        )
        assert num_placeholders == len(dynamo_source_info)
        for node in gm_serializer.graph.nodes:
            if node.op != "placeholder":
                break
            source_info = dynamo_source_info[node.name]
            node._dynamo_source = _dynamo_source_dict_to_class(Source, source_info)

    gm = GraphModule(gm_serializer.module, gm_serializer.graph)
    if fill_tensor_meta:
        fill_tensor_meta_from_val_meta(gm)

    return gm
