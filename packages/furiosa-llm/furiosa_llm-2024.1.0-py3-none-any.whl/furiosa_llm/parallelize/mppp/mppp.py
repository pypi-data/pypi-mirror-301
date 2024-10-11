from abc import ABC, abstractmethod
import typing
from typing import Any, Mapping, Optional, Sequence, Union

from furiosa_llm.parallelize.block_slicer import (
    get_block_slicing_edges,
    get_blockwise_sliced_color_map,
)
from furiosa_llm.parallelize.pipeline_builder.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.pipeline_builder.trace import get_aten_graph_with_original_names
from furiosa_llm.parallelize.utils import (
    gen_mppp_config_with_no_parallelism,
    get_original_model_type,
)

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata

import torch
from torch.fx import GraphModule
from transformers import PretrainedConfig

from furiosa_llm.models import ModelMetadata
from furiosa_llm.parallelize.config import (
    Device,
    DeviceId,
    DeviceMesh,
    DynamicTensorSpec,
    MpppConfig,
    Replicate,
    ShardSpec,
)


class Mppp(ABC):

    @abstractmethod
    def gen_config(
        self,
        model: Union[torch.nn.Module, "ModelMetadata"],
        # TODO: remove model_config parameter
        model_config: PretrainedConfig,
        devices: Sequence[Device],
        example_args: Sequence[Any],
        example_kwargs: Mapping[str, Any],
        graph_module: Optional[GraphModule] = None,
        other_configs: Mapping[str, Any] = {},
    ) -> MpppConfig:
        raise NotImplementedError("Mppp Should implement gen_config method")


class DefaultMppp(Mppp):
    def __init__(self) -> None: ...

    def gen_config(
        self,
        model: Union[torch.nn.Module, "ModelMetadata"],
        # TODO: remove model_config parameter
        model_config: PretrainedConfig,
        devices: Sequence[Device],
        example_args: Sequence[Any],
        example_kwargs: Mapping[str, Any],
        graph_module: Optional[GraphModule] = None,
        other_configs: Mapping[str, Any] = {},
    ) -> MpppConfig:
        # FIXME: remove monkey patch and replace this with general strategy finding logic.
        raise NotImplementedError(f"Mppp doesn't support {model.__class__} model yet")


def gen_pp_mpc(
    model: Union[torch.nn.Module, ModelMetadata],
    devices: Sequence[Device],
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
    graph_module: Optional[GraphModule] = None,
) -> MpppConfig:
    """Generate Pipeline Parallelism Mppp Config for ``model``, running with ``devices``."""
    if graph_module is None:
        # `graph_module` is not given and model is `ModelMetadata`. Instantiate model.
        if isinstance(model, ModelMetadata):
            use_random_weight = model.is_random_weight_only_model()
            model_: Union[torch.nn.Module, ModelCreationInfo] = ModelCreationInfo(
                model,
                use_random_weight,
                0,
            )
        else:
            model_ = model
        gm, _ = get_aten_graph_with_original_names(
            model_,
            args,
            kwargs,
        )
    else:
        gm = graph_module

    if isinstance(model, torch.nn.Module):
        original_model_type = get_original_model_type(model)
    else:
        original_model_type = model.get_optimized_cls()

    pp_level = len(devices)
    n_layer = model.config.num_hidden_layers
    if n_layer % pp_level != 0:
        raise NotImplementedError(
            "Mppp Config cannot be generated for the case when number of transformer blocks is not a multiple of pipeline parallelism level."
        )
    n_layer_per_pp_stage = n_layer // pp_level

    if pp_level == 1:
        assert len(devices) == 1
        # No parallelism
        return gen_mppp_config_with_no_parallelism(f"{original_model_type}-no-pp", gm, devices[0])

    split_edges = get_block_slicing_edges(gm, original_model_type)

    assert len(split_edges) == n_layer
    block_idx_map = get_blockwise_sliced_color_map(gm, split_edges, mark_color_to_meta=False)
    # Node name to belonging pp stages.
    pp_stage_map = {
        node_name: set(color // n_layer_per_pp_stage for color in colors)
        for node_name, colors in block_idx_map.items()
    }

    dynamic_tensors = []
    static_tensors = {}
    mppp_devices = {DeviceId(str(i)): device for i, device in enumerate(devices)}

    for node in gm.graph.nodes:
        if not node.all_input_nodes:
            device_ids = [DeviceId(str(stage_num)) for stage_num in pp_stage_map[node.name]]
            static_tensors[node.name] = ShardSpec([Replicate()], DeviceMesh(device_ids))

    for node in gm.graph.nodes:
        parent_stages = pp_stage_map[node.name]
        for user in node.users:
            if user.op == "output":
                continue
            child_stages = pp_stage_map[user.name]
            # If stages are different, need repartitioning.
            if child_stages != parent_stages:
                # color is different. need repartitioning
                child_device_mesh = DeviceMesh(
                    [DeviceId(str(stage_num)) for stage_num in child_stages]
                )
                dynamic_tensors.append(
                    DynamicTensorSpec(
                        src=node.name,
                        dst=user.name,
                        spec=ShardSpec([Replicate()], child_device_mesh),
                    )
                )
    mppp_config = MpppConfig(
        f"{original_model_type}-pp{len(devices)}",
        devices=mppp_devices,
        static_tensors=static_tensors,
        dynamic_tensors=dynamic_tensors,
    )
    return mppp_config


class PipelineParallelismMppp(Mppp):
    def __init__(self) -> None: ...

    def gen_config(
        self,
        model: Union[torch.nn.Module, ModelMetadata],
        _model_config: PretrainedConfig,
        devices: Sequence[Device],
        example_args: Sequence[Any],
        example_kwargs: Mapping[str, Any],
        graph_module: Optional[GraphModule] = None,
        _other_configs: Mapping[str, Any] = {},
    ) -> MpppConfig:
        return gen_pp_mpc(model, devices, example_args, example_kwargs, graph_module=graph_module)
