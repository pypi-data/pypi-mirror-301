import abc
import copy
from enum import Enum
from functools import cached_property
import glob
from itertools import product
import json
import logging
import operator
import os
from pathlib import Path
import re
import sys
import tempfile
from time import time
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    get_args,
)
import uuid

from furiosa_torch_ext.torch_ext import preprocess
from pydantic import BaseModel, RootModel
from pydantic.dataclasses import dataclass
import ray
from torch import nn
from torch._subclasses import FakeTensorMode
import torch.distributed._tensor.ops.common_rules
from torch.fx import GraphModule
from torch.fx.passes.shape_prop import ShapeProp
import transformers
from transformers import (
    MODEL_FOR_CAUSAL_LM_MAPPING,
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    set_seed,
)
import yaml

from furiosa_llm.hash import hash_model
from furiosa_llm.parallelize.config import DeviceId
from furiosa_llm.parallelize.mppp import PipelineParallelismMppp
from furiosa_llm.parallelize.pipeline.types import (
    CompSuperTask,
    DataBlobId,
    Device,
    ParamfileFormat,
    ParamFileInfo,
    ParamInfo,
    PipelineMode,
    SuperTaskKind,
    TensorInfo,
)
from furiosa_llm.parallelize.pipeline_builder.converter import GraphModuleConverter
from furiosa_llm.parallelize.pipeline_builder.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.pipeline_builder.serialize import deserialize_gm
from furiosa_llm.parallelize.pipeline_builder.utils import write_without_concurrency_issue
from furiosa_llm.parallelize.utils import load_partial_param
from furiosa_llm.utils import generate_input_sample, get_cache_path_if_exists, zip_equal

from .compiler_config import CompilerConfigContext
from .device import fusion_pes, normalize_devices_into_single_pes, parse_devices_str
from .models import (
    AttentionType,
    Bucket,
    KvCacheSharingAcrossBeamsConfig,
    LLMConfig,
    ModelMetadata,
    OptimizationConfig,
    PagedAttentionConfig,
    get_model_cls_from_pretrained_id,
)
from .outputs import CompletionOutput, RequestOutput
from .parallelize.mppp import Mppp
from .parallelize.pipeline import Pipeline
from .parallelize.pipeline_builder import PipelineBuilder
from .sampling_params import SamplingParams
from .tokenizer import encode_auto, get_tokenizer

logger = logging.getLogger(__name__)

# Workaround for this release. This will be removed in the next release.
os.environ["NPU_ARCH"] = "renegade"

# Default position id for padding
_POSITION_ID_PAD = 1

# Default param file name
_PARAM_FILE_NAME = "params.safetensors"
_HF_CAUSAL_LM_CLASS_NAMES = set(
    model_cls.__name__ for model_cls in MODEL_FOR_CAUSAL_LM_MAPPING.values()
)

# Default index of the padding block when paged attention model is used.
DEFAULT_PAGED_ATTENTION_PADDING_BLOCK_IDX = 0

CACHE_DIR = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")) / "furiosa" / "llm"

STR_TO_TORCH_DTYPE = {
    "int8": torch.int8,
    "bf16": torch.bfloat16,
    "fp32": torch.float32,
    # NOTE: We decided to use torch.int8 to represent fp8  in compression stack.
    "fp8-E4M3": torch.int8,
}

TokenizerModeType = Literal["auto", "slow"]

RAY_LOG_PREFIX = "[furiosa-llm]"

STREAMING_MAX_DECODE_TRIAL = 2


@dataclass
class SchedulerConfig:
    """
    * npu_queue_limit: Maximum number of tasks that can be queued in the hardward
    * max_processing_samples: Maximum number of samples that can be processed by the scheduler
    * spare_blocks_ratio: Ratio of spare blocks that are reserved by scheduler. Smaller value will force the scheduler to use dram aggressively
    * is_offline: If True, use strategies optimzed for offline scenario
    """

    npu_queue_limit: int = 2
    max_processing_samples: int = 65536
    spare_blocks_ratio: float = 0.2
    is_offline: bool = False

    # custom comparator to handle float comparison
    def __eq__(self, other):
        return (
            self.npu_queue_limit == other.npu_queue_limit
            and self.max_processing_samples == other.max_processing_samples
            and abs(self.spare_blocks_ratio - other.spare_blocks_ratio) < 1e-6
            and self.is_offline == other.is_offline
        )


@dataclass
class GeneratorConfig:
    position_id_pad: int
    prefill_buckets: Sequence[Bucket]
    decode_buckets: Sequence[Bucket]
    model_qname: str  # qualified name of the model (module + class)
    paged_attention_config: Optional[PagedAttentionConfig]
    packing_type: Literal["IDENTITY"]
    kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig]
    scheduler_config: Optional[SchedulerConfig]

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w") as f:
            f.write(RootModel[GeneratorConfig](self).model_dump_json(indent=4))

    @classmethod
    def load(cls, path: Union[str, os.PathLike]):
        with open(path) as f:
            o = json.load(f)
            return GeneratorConfig(**o)


class LLMBackend(Enum):
    """The backend implementation to run forward() of a model for the LLM."""

    # FIXME: In order to increase the code consistency, use the capital letter for the enum value
    TORCH_PIPELINE_RUNNER = "torch_pipeline_runner"
    FURIOSA_RT_CUDA = "furiosa_rt_cuda"
    FURIOSA_RT_NPU = "furiosa_rt_npu"
    TORCH_V2 = "torch_v2"
    FURIOSA_RT_V2 = "furiosa_rt_v2"
    MOCK_BACKEND_V2 = "mock_backend_v2"

    def is_parallelism_supported(self) -> bool:
        """Tensor Parallelism/Pipeline Parallelism supports"""
        return self in (
            LLMBackend.TORCH_PIPELINE_RUNNER,
            LLMBackend.FURIOSA_RT_CUDA,
            LLMBackend.FURIOSA_RT_NPU,
            LLMBackend.TORCH_V2,
            LLMBackend.FURIOSA_RT_V2,
            LLMBackend.MOCK_BACKEND_V2,
        )

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls[value.upper()]


def _get_example_input(
    supertask: CompSuperTask,
    pipeline: Pipeline,
    fake_mode: FakeTensorMode,
) -> Tuple[torch.Tensor, ...]:
    with fake_mode:
        return tuple(
            torch.zeros(
                pipeline.tensors[input_].shape,
                dtype=pipeline.tensors[input_].dtype.to_torch_dtype(),
            )
            for input_ in supertask.inputs
        )


# IMPORTANT: Compiler config generation part part in this function must be kept same as `GraphModuleConverter._get_data_blob_id`.
def _compile_supertasks_in_pipeline(
    pipeline: Pipeline,
    target_ir: str,
    # current context: model_qname, beam_size, phase, bucket
    compiler_config_context: CompilerConfigContext,
    serialize_compiled_graphs: bool = False,
) -> None:
    fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

    compiled_blobs = set()
    # Dump an intermediate artifact (e.g., DFG, ir graphs, dot graphs) for debugging purpose
    dump_path = os.getenv("FURIOSA_COMPILE_DUMP_PATH")

    for supertask_id, supertask in pipeline.supertasks.items():
        if not isinstance(supertask, CompSuperTask):
            continue
        if supertask.kind != SuperTaskKind.FX:
            raise NotImplementedError("Supertask kind other than FX cannot be compiled now")
        if supertask.data_blob is not None:
            if supertask.data_blob in compiled_blobs:
                # already compiled
                supertask.kind = SuperTaskKind.from_str(target_ir)
                continue
            blob = pipeline.blobs[supertask.data_blob]
        else:
            assert isinstance(supertask.data, str)
            blob = supertask.data

        gm = deserialize_gm(blob)
        example_input = _get_example_input(supertask, pipeline, fake_mode)
        target_npu = GraphModuleConverter.get_target_npu_from_device(
            pipeline.devices[supertask.device]
        )

        _info_log_for_ray(
            f"Compiling pipeline {pipeline.name}, supertask {supertask_id} for {target_npu}."
        )

        compiler_config = None
        compiler_config_context = copy.deepcopy(compiler_config_context)
        num_pe = pipeline.devices[supertask.device].num_pe
        compiler_config_context.num_pe = num_pe

        block_type = pipeline.get_block_type_from_supertask_id(supertask_id)
        num_pe = pipeline.devices[supertask.device].num_pe
        logger.info("Block type: %s", block_type)

        compiler_config_context = copy.deepcopy(compiler_config_context)
        compiler_config_context.block_type = block_type
        compiler_config_context.num_pe = num_pe

        compiler_config = compiler_config_context.load_config()
        logger.info(f"Using compiler config {compiler_config}")

        compiled = GraphModuleConverter.compile_gm(
            gm,
            example_input,
            target_npu,
            target_ir,
            compiler_config,
            supertask.data_blob,
            dump_path,
        )
        _info_log_for_ray(
            f"Finished compiling pipeline {pipeline.name}, supertask {supertask_id} for {target_npu}."
        )

        if serialize_compiled_graphs:
            compiled = compiled.serialize()

        if supertask.data_blob is not None:
            # replace data_blobs
            pipeline.blobs[supertask.data_blob] = compiled
            compiled_blobs.add(supertask.data_blob)
        else:
            supertask.data = compiled
        supertask.kind = SuperTaskKind.from_str(target_ir)


def _info_log_for_ray(msg: str):
    logger.info(f"[furiosa-llm] {msg}")


# Better name?
def _get_parallel_mesh(
    devices: Sequence[Device],
    tensor_parallel_size: int,
    pipeline_parallel_size: int,
    data_parallel_size: Optional[int] = None,
) -> List[List[List[Device]]]:
    """Get parallel 3d mesh for given devices and parallelism degrees, whose dimesions corresponds to dp, pp, and tp respectively."""

    # Create tensor parllelism_groups
    is_npu = devices[0].kind == "npu"

    if is_npu:
        if (
            tensor_parallel_size
            not in (
                1,
                2,
                4,
            )
            and tensor_parallel_size % 8 != 0
        ):
            raise ValueError("Tensor parallelism degree must be 1, 2, 4, or multiples of 8.")

        # TODO: add support for tensor parallelism.
        if tensor_parallel_size > 4:
            raise NotImplementedError(
                "Tensor parallelism with more than 4 pes is not supported yet."
            )

    minimal_pus: List[Device]

    if is_npu:
        # In case of npu, parallelism strategy is defined in pe granularity.
        minimal_pus = normalize_devices_into_single_pes(devices)
    else:
        minimal_pus = list(devices)
    data_parallel_size = data_parallel_size or len(minimal_pus) // (
        pipeline_parallel_size * tensor_parallel_size
    )

    if len(minimal_pus) != data_parallel_size * pipeline_parallel_size * tensor_parallel_size:
        raise ValueError(
            "The number of PEs must be eqaul to the product of tensor_parallel size, pipeline_parallel_size, and data_parallel_size."
        )

    if is_npu:
        # Fusion PEs according to the tensor_parallel_size if the device is npu.
        fusion_granularity = tensor_parallel_size if tensor_parallel_size < 4 else 4

        fusioned_pes = [
            fusion_pes(minimal_pus[start : start + fusion_granularity])
            for start in range(0, len(minimal_pus), fusion_granularity)
        ]

        across_fusioned_pe_tp_degree = tensor_parallel_size // fusion_granularity
        assert len(fusioned_pes) % across_fusioned_pe_tp_degree == 0

        # 2d-matrix (list of tp groups)
        tp_groups = [
            fusioned_pes[start : start + across_fusioned_pe_tp_degree]
            for start in range(0, len(fusioned_pes), across_fusioned_pe_tp_degree)
        ]
    else:
        # Otherwise, there's no fusion.
        if tensor_parallel_size != 1:
            raise NotImplementedError("Tensor parallelism across chips is not supported yet.")
        fusioned_pes = minimal_pus

        # 2d-matrix (list of tp groups)
        tp_groups = [
            fusioned_pes[start : start + tensor_parallel_size]
            for start in range(0, len(fusioned_pes), tensor_parallel_size)
        ]

    used = set()
    dp_pp_tp_groups = []

    # create pp groups, each of which consists of multiple tp groups. List of pp groups naturally become dp group.
    for _ in range(data_parallel_size):
        cur_pp_group: List[List[Device]] = []
        while len(cur_pp_group) < pipeline_parallel_size:
            # Add not used tp_group to pp group
            cur_last_device_npu_idx = cur_pp_group[-1][-1].idx if len(cur_pp_group) > 0 else -1
            for i in range(len(tp_groups)):
                if i in used or cur_last_device_npu_idx >= tp_groups[i][0].idx:
                    continue
                cur_pp_group.append(tp_groups[i])
                used.add(i)
                break
            else:
                raise ValueError(
                    "Cannot form a proper pp group with current option. Pipeline parallelism across pes on same device has no benefit."
                )
        dp_pp_tp_groups.append(cur_pp_group)

    return dp_pp_tp_groups


class BucketConfig(abc.ABC): ...


@dataclass
class ManualBucketConfig(BucketConfig):
    prefill_buckets: Sequence[Tuple[int, int]]
    decode_buckets: Optional[Sequence[Tuple[int, int]]] = None


@dataclass
class MinimalBucketConfig(BucketConfig):
    max_seq_len: int


def _get_available_devices() -> List[Device]:
    try:
        from furiosa_smi_py import (  # type: ignore[import-not-found, import-untyped]
            CoreStatus,
            list_devices,
        )
    except ImportError:
        raise ImportError("Install furiosa_smi_py to get available devices automatically.")

    try:
        devices = list_devices()
        available_devs = []
        for device in devices:
            # e.g. /dev/rngd/npu1
            name = device.device_info().name()
            npu_idx = int(name.rsplit("/", 1)[-1][-1])
            core_status = device.core_status()

            for core_id, status in core_status.items():
                # Cannot be compared by reference (using "is") because `CoreStatus` is a Rust enum exposed with PyO3.
                if status == CoreStatus.Available:
                    available_devs.append(Device(f"npu:{npu_idx}:{core_id}"))
        return available_devs
    except Exception as e:
        raise RuntimeError(f"Failed to get available devices with errror {e}")


def _get_bucket_from_pipeline_name(pipeline_name: str) -> Tuple[bool, Bucket]:
    # Returns: tuple of (is_prefill, bucket)
    # pipeline name = f"{model_name}-{mode}-b{bucket.batch_size}-attn{bucket.attention_size}
    _, mode, b_batch_size, attn_attn_size = pipeline_name.split("-")

    is_prefill = mode == "prefill"

    batch_size = int(b_batch_size[1:])
    attn_size = int(attn_attn_size[4:])

    return is_prefill, Bucket(batch_size, attn_size)


class ModelRewritingConfig(BaseModel):
    do_decompositions_for_model_rewrite: bool
    use_blockwise_compile: bool
    num_blocks_per_supertask: int
    embed_all_constants_into_graph: bool


class ParallelConfig(BaseModel):
    tensor_parallel_size: int
    pipeline_parallel_size: int


class LLM:
    """An LLM for generating texts from given prompts and sampling parameters.

    Args:
        pretrained_id: The name of the pretrained model. This corresponds to
            pretrained_model_name_or_path in HuggingFace Transformers.
        task_type: The type of the task. This corresponds to task in HuggingFace Transformers.
            See https://huggingface.co/docs/transformers/main/en/quicktour#pipeline for more
            details.
        llm_config: The configuration for the LLM. This includes quantization and optimization
            configurations.
        qformat_path: The path to the quantization format file.
        qparam_path: The path to the quantization parameter file.
        prefill_quant_bin_path: The path to the quantziation prefill bin file.
        decode_quant_bin_path: The path to the quantziation decode bin file.
        config: The configuration for the HuggingFace Transformers model. This is a dictionary
            that includes the configuration for the model.
        bucket_config: Config for bucket generating policy. If not given, the model will use single one batch, `max_seq_len_to_capture` attention size bucket per
            each phase.
        max_seq_len_to_capture: Maximum sequence length covered by LLM engine. Sequence with larger context than this will not be covered.
            The default is 2048.
        tensor_parallel_size: The number of PEs for each tensor parallelism group. The default is 4.
        pipeline_parallel_size: The number of pipeline stages for pipeline parallelism. The default is 1,
            which means no pipeline parallelism.
        data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
            total avaialble PEs and other parallelism degrees.
        tokenizer: The name or path of a HuggingFace Transformers tokenizer.
        tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
            if available, and "slow" will always use the slow tokenizer.
        seed: The seed to initialize the random number generator for sampling.
        devices: The devices to run the model. It can be a single device or a list of devices.
            Each device can be either "npu:X" or "npu:X:*" where X is a specific device index.
            If not given, available devices will be used.
        param_file_path: The path to the parameter file to use for pipeline generation.
            If not specified, the parameters will be saved in a temporary file which will be
            deleted when ``LLM`` is destroyed.
        param_saved_format: The format of the parameter file. Only possible value is "safetensors" now.
            The default is "safetensors".
        do_decompositions_for_model_rewrite: Whether to decompose some ops to describe various parallelism strategies
            with mppp config. When the value is True, mppp config that matches with the decomposed FX graph should be given.
        comp_supertask_kind: The format that pipeline's supertasks will be represented as.
            Possible values are "fx","dfg", and "edf", and the default is "edf".
        cache_dir: The cache directory for all generated files for this LLM instance.
            When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
        backend: The backend implementation to run forward() of a model for the LLM.
            If not specified, the backend will be chosen based on the device kind.
        use_blockwise_compile: If True, each task will be compiled in the unit of transformer block,
            and compilation result for transformer block is generated once and reused. The default is ``True``.
        num_blocks_per_supertask: The number of transformer blocks that will be merged into one supertask. This option is valid
            only when `use_blockwise_compile=True`. The default is 1.
        embed_all_constants_into_graph: Whether to embed constant tensors into graph or make them as input of the graph and save them as separate files.
            The default is False.
        paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store. This argument must be given
            if model uses paged attention. This argument must be given if model uses paged attention.
        paged_attention_block_size: The maximum number of tokens that can be stored in a single paged attention block. This argument must be given
            if model uses paged attention.
        kv_cache_sharing_across_beams_config: Configuration for sharing kv cache across beams. This argument must be given if and only if
            the model is optimized to share kv cache across beams. If this argument is given, decode phase buckets with batch size of
            ``batch_size`` * ``kv_cache_sharing_across_beams_config.beam_width`` will be created.
        scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
            that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler.
        packing_type: Packing algorithm. Possible values are "IDENTITY" only for now
        compiler_config_overrides: Overrides for the compiler config. This is a dictionary that includes the configuration for the compiler.
        use_random_weight: If True, the model will be initialized with random weights.
        num_pipeline_builder_workers: number of workers used for building pipelines (except for compilation). The default is 1 (no parallelism).
            Setting this value larger than 1 reduces pipeline building time, especially for large models, but requires much more memory.
        num_compile_workers: number of workers used for compilation. The default is 1 (no parallelism).
        skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
            the pipelines for other purposes than running them with the engine.
        artifacts_export_path: The path to export the artifacts. With artifacts, you can create ``LLM`` without quantizing or compiling the model again.
    """

    def __init__(
        self,
        model: str,
        task_type: Optional[str] = None,
        llm_config: Optional[LLMConfig] = None,
        qformat_path: Optional[os.PathLike] = None,  # FIXME: move to quantization_config
        qparam_path: Optional[os.PathLike] = None,  # FIXME: move to quantization_config
        prefill_quant_bin_path: Optional[os.PathLike] = None,
        decode_quant_bin_path: Optional[os.PathLike] = None,
        config: Dict[str, Any] = {},  # aka hf_config
        bucket_config: Optional[BucketConfig] = None,
        max_seq_len_to_capture: int = 2048,
        tensor_parallel_size: int = 4,
        pipeline_parallel_size: int = 1,
        data_parallel_size: Optional[int] = None,
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        seed: Optional[int] = None,
        # TODO: change devices default value to None and get devices from furiosa-smi.
        devices: Optional[Union[str, Sequence[Device]]] = None,
        param_file_path: Optional[os.PathLike] = None,
        param_saved_format: Literal["safetensors", "pt"] = "safetensors",
        do_decompositions_for_model_rewrite: bool = False,  # FIXME: move to compiler_config
        comp_supertask_kind: Optional[Literal["edf", "dfg", "fx"]] = None,
        cache_dir: Optional[os.PathLike] = CACHE_DIR,
        backend: Optional[LLMBackend] = None,
        use_blockwise_compile: bool = True,  # FIXME: move to compiler_config
        num_blocks_per_supertask: int = 1,  # FIXME: move to compiler_config
        embed_all_constants_into_graph: bool = False,
        paged_attention_num_blocks: Optional[int] = None,  # FIXME: move to compiler_config
        paged_attention_block_size: int = 1,  # FIXME: move to compiler_config
        kv_cache_sharing_across_beams_config: Optional[
            KvCacheSharingAcrossBeamsConfig
        ] = None,  # FIXME: move to compiler_config / leave this in LLM attr ??
        scheduler_config: SchedulerConfig = SchedulerConfig(),
        packing_type: Literal["IDENTITY"] = "IDENTITY",
        compiler_config_overrides: Optional[Mapping] = None,
        use_random_weight: bool = False,
        num_pipeline_builder_workers: int = 1,
        num_compile_workers: int = 1,
        skip_engine: bool = False,
        artifacts_export_path: Optional[Union[str, os.PathLike]] = None,
        *,
        _cleanup: bool = True,
        _pipelines: Optional[Sequence[Pipeline]] = None,
        **kwargs,
    ):
        optimize_paged_attention_block_loading = kwargs.pop(
            "optimize_paged_attention_block_loading", True
        )
        sparse_select_version = kwargs.pop("sparse_select_version", "v1.5")
        one_supertask_per_device = kwargs.pop("one_supertask_per_device", True)

        if artifacts_export_path:
            os.environ["FURIOSA_COMPILE_DUMP_PATH"] = str(artifacts_export_path)

        # Set seed in order to guarantee the reproducibility with the same seed number
        if seed is not None:
            set_seed(seed)

        LLM.__verify_tokenizer_mode(tokenizer_mode)

        # Set logging options for ray.
        if "RAY_COLOR_PREFIX" not in os.environ:
            os.environ["RAY_COLOR_PREFIX"] = "1"
        if "RAY_DEDUP_LOGS_ALLOW_REGEX" not in os.environ:
            # For not to dedup our info logs.
            os.environ["RAY_DEDUP_LOGS_ALLOW_REGEX"] = f"INFO:*{RAY_LOG_PREFIX}*"

        if devices is None:
            devices = _get_available_devices()

        assert devices is not None

        # Normalize the devices
        if isinstance(devices, str):
            devices = parse_devices_str(devices)
        LLM.__verify_devices(devices)

        if num_pipeline_builder_workers < 1:
            raise ValueError("`num_pipeline_builder_workers` must be larger than 0")

        if llm_config is None:
            llm_config = self._get_default_llm_config_from_pretrained_id(model)

        self.model_metadata = ModelMetadata(
            pretrained_id=model,
            task_type=task_type,
            llm_config=llm_config,
            hf_configs=config.copy(),
        )

        self.model_config = self.model_metadata.config
        self.is_generative_model = self.model_metadata.is_generative_model
        kv_cache_dtype = self.model_metadata.kv_cache_dtype

        if bucket_config is None:
            if max_seq_len_to_capture > self.model_max_seq_len:
                raise ValueError(
                    "`max_seq_len_to_capture` is larger than the model's max number of positions."
                )
            # TODO: alaways set max_seq_len to model's max_position_embeddings once compiler supports it.
            bucket_config = MinimalBucketConfig(max_seq_len=max_seq_len_to_capture)

        buckets_for_prefill, buckets_for_decode = self._get_buckets(bucket_config)

        # filter out buckets that are larger than max_seq_len_to_capture
        buckets_for_prefill = [
            bucket
            for bucket in buckets_for_prefill
            if bucket.attention_size <= max_seq_len_to_capture
        ]
        buckets_for_decode = [
            bucket
            for bucket in buckets_for_decode
            if bucket.attention_size <= max_seq_len_to_capture
        ]

        logger.info(f"Prefill buckets: {buckets_for_prefill}")
        logger.info(f"Decode buckets: {buckets_for_decode}")

        LLM.__verify_buckets(
            buckets_for_prefill, buckets_for_decode, kv_cache_sharing_across_beams_config
        )

        if (
            self.model_metadata.optimize_options.kv_cache_sharing_across_beams
            and kv_cache_sharing_across_beams_config is None
        ):
            raise ValueError(
                "`kv_cache_sharing_across_beams_config` must be given if the model is optimized to share kv cache across beams."
            )

        padding_block_idx = (
            DEFAULT_PAGED_ATTENTION_PADDING_BLOCK_IDX
            if optimize_paged_attention_block_loading
            else None
        )

        if self.model_metadata.attention_type is AttentionType.PAGED_ATTENTION:
            if paged_attention_num_blocks is None:
                # TODO: if `paged_attention_num_blocks` is not given, always calculate maximum possible num blocks and use that.
                raise NotImplementedError(
                    "`paged_attention_num_blocks` must be given for paged attention models now."
                )
            if paged_attention_block_size != 1:
                raise NotImplementedError(
                    "Currently, only paged attention with block_size=1 is supported."
                )
            assert paged_attention_num_blocks is not None
            paged_attention_config = PagedAttentionConfig(
                paged_attention_num_blocks, paged_attention_block_size, padding_block_idx
            )
        else:
            paged_attention_config = None

        original_model_type = self.model_metadata.get_optimized_cls()
        self.generator_config = GeneratorConfig(
            _POSITION_ID_PAD,
            buckets_for_prefill,
            buckets_for_decode,
            f"{original_model_type.__module__}.{original_model_type.__name__}",
            paged_attention_config,
            packing_type,
            kv_cache_sharing_across_beams_config,
            scheduler_config,
        )

        self.model_rewriting_config = ModelRewritingConfig(
            do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
            use_blockwise_compile=use_blockwise_compile,
            num_blocks_per_supertask=num_blocks_per_supertask,
            embed_all_constants_into_graph=embed_all_constants_into_graph,
        )

        if device_sets_for_actual_use := kwargs.pop("device_sets_for_actual_use", None):
            logger.warning(
                "`device_sets_for_actual_use` is deprecated. Use `{tensor|pipeline|data}_parallel` options instead."
            )
            normalized_dev_mesh = [
                parse_devices_str(device_set) if isinstance(device_set, str) else device_set
                for device_set in device_sets_for_actual_use
            ]
        else:
            dev_mesh = _get_parallel_mesh(
                devices, tensor_parallel_size, pipeline_parallel_size, data_parallel_size
            )
            # Flatten pp_tp_groups to build pipeline. This is 2d-matrix whose elements are dp subgroups.
            normalized_dev_mesh = [
                [dev for tp_group in pp_tp_group for dev in tp_group] for pp_tp_group in dev_mesh
            ]

        self.parallel_config = ParallelConfig(
            tensor_parallel_size=tensor_parallel_size, pipeline_parallel_size=pipeline_parallel_size
        )

        data_parallel_size = len(normalized_dev_mesh)

        # Build pipelines for first pp_tp_group and replicate them for other pp_tp_groups later.
        first_dp_subgroup_devices = normalized_dev_mesh[0]

        if backend is None:
            dev_kind = devices[0].kind
            if dev_kind == "npu":
                backend = LLMBackend.FURIOSA_RT_V2
            elif dev_kind == "cpu":
                backend = LLMBackend.TORCH_V2
            elif dev_kind == "cuda":
                backend = LLMBackend.FURIOSA_RT_CUDA
            else:
                raise ValueError(f"Invalid device kind: {dev_kind}")

        if comp_supertask_kind is None:
            if backend in (LLMBackend.FURIOSA_RT_NPU, LLMBackend.FURIOSA_RT_V2):
                comp_supertask_kind = "edf"
            else:
                comp_supertask_kind = "fx"
        if comp_supertask_kind == "dfg":
            logger.info("Using dfg as comp_supertask_kind")
        LLM.__verify_comp_supertask_kind(comp_supertask_kind)

        model_ = ModelCreationInfo(
            self.model_metadata,
            use_random_weight,
            seed,
            qformat_path=qformat_path,
            qparam_path=qparam_path,
            prefill_quant_bin_path=prefill_quant_bin_path,
            decode_quant_bin_path=decode_quant_bin_path,
        )

        beam_size_or_none = (
            None
            if self.generator_config.kv_cache_sharing_across_beams_config is None
            else self.generator_config.kv_cache_sharing_across_beams_config.beam_width
        )

        compiler_config_context = CompilerConfigContext(
            model_qname=str(self.model_metadata),
            beam_size=beam_size_or_none,
            compiler_config_overrides=compiler_config_overrides,
        )

        # Get Tokenizer
        self.tokenizer = get_tokenizer(
            self.model_config.name_or_path, tokenizer, tokenizer_mode, **kwargs
        )

        # Please refer to an example at https://huggingface.co/docs/transformers/en/main_classes/text_generation#transformers.GenerationMixin.greedy_search.example
        # Some models like GPT-2 may not have pad_token_id. BTW, when we run a batch of sequence generations,
        # We must need pad_token_id to fill the batch with pad. With Hugging Face Transformers,
        # users should handle this issue. Our goal is to provide a better useability for users.
        # We handle this issue within LLM class.
        self.model_config.pad_token_id = self.model_config.eos_token_id

        if _pipelines is not None:
            # FIXME: This pass exists only for supporting `LLM.from_artifacts` API.

            # Only pick pipelines for given buckets.
            buckets_to_include = {
                *[(True, bucket) for bucket in self.generator_config.prefill_buckets],
                *[(False, bucket) for bucket in self.generator_config.decode_buckets],
            }

            pipelines_with_bucket_info = [
                (_get_bucket_from_pipeline_name(pipeline.name), pipeline) for pipeline in _pipelines
            ]

            pipelines = [
                pipeline
                for (is_prefill, bucket), pipeline in pipelines_with_bucket_info
                if (is_prefill, bucket) in buckets_to_include
            ]

            # replace devices in pipelines
            for pipeline in pipelines:
                if len(pipeline.devices) != len(first_dp_subgroup_devices):
                    raise ValueError(
                        "The number of devices in the pipeline is different from the number of devices in the first dp subgroup."
                    )

                pipeline.devices = {
                    DeviceId(str(i)): dev for i, dev in enumerate(first_dp_subgroup_devices)
                }

            self.pipelines = pipelines
        else:
            if self.is_generative_model and self.model_metadata.is_quantized:
                assert kv_cache_dtype is not None
                qformat_path_ = (
                    qformat_path if qformat_path else self.model_metadata.qformat_qparam_path()[0]
                )
                self.__verify_kv_cache_dtype_with_qformat(
                    kv_cache_dtype, qformat_path_, self.model_metadata
                )

            self.build_all_pipelines(
                model_,
                first_dp_subgroup_devices,
                backend,
                comp_supertask_kind,
                use_random_weight,
                qformat_path,
                qparam_path,
                one_supertask_per_device,
                use_blockwise_compile,
                do_decompositions_for_model_rewrite,
                kv_cache_dtype,
                sparse_select_version,
                num_pipeline_builder_workers,
                num_compile_workers,
                embed_all_constants_into_graph,
                num_blocks_per_supertask,
                param_file_path,
                param_saved_format,
                compiler_config_context,
                cache_dir,
                _cleanup,
            )

            # Save artifacts berfoe copying pipelines according to `data_parallelism_size`.
            if artifacts_export_path:
                self._save_engine_artifacts(
                    artifacts_export_path,
                    comp_supertask_kind,
                    devices,
                )

        # If data parallelism is used, replicate pipelines for each entity data parallelism subgroup.
        if data_parallel_size > 1:
            self.pipelines: List[Pipeline] = [  # type: ignore[no-redef]
                pipeline.shallow_copy_with_replaced_devices(
                    dict(zip_equal(first_dp_subgroup_devices, flattened_pp_tp_group))  # type: ignore[arg-type]
                )
                for pipeline, flattened_pp_tp_group in product(self.pipelines, normalized_dev_mesh)
            ]

        # for e2e testing purpose, it allows to skip to initialize the engine
        if not skip_engine:
            try:
                from furiosa.native_runtime.llm import NativeLLMEngine  # type: ignore
            except ImportError:
                logger.error(
                    "NativeLLMEngine is not available. Please make sure that the furiosa-native-runtime is installed.\n"
                    'You can install furiosa-native-runtime by running `pip install "furiosa-llm[full]"`.\n'
                    "If you want to use the LLM without the native runtime, you can set `skip_engine=True` in the constructor."
                )
                raise

            self.engine = NativeLLMEngine(
                self.pipelines,
                self.generator_config,
                backend=backend.value,
                hf_config=self.model_config,
            )

    @classmethod
    def from_artifacts(
        cls,
        path: Union[str, os.PathLike],
        bucket_config: Optional[BucketConfig] = None,
        data_parallel_size: Optional[int] = None,
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        seed: Optional[int] = None,
        devices: Optional[Union[str, Sequence[Device]]] = None,
        cache_dir: os.PathLike = CACHE_DIR,
        backend: Optional[LLMBackend] = None,
        paged_attention_num_blocks: Optional[int] = None,
        scheduler_config: SchedulerConfig = SchedulerConfig(),
        packing_type: Literal["IDENTITY"] = "IDENTITY",
        skip_engine: bool = False,
        *,
        _cleanup: bool = True,
        **kwargs,
    ) -> "LLM":
        """Instantiate LLM from saved artifacts without quantization and compilation.

        Args:
            path: A path to artifacts to load.
            bucket_config: Config for bucket generating policy. If not given, all buckets in the artifacts will be used.
            data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
                total avaialble PEs and other parallelism degrees.
            tokenizer: The name or path of a HuggingFace Transformers tokenizer.
            tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
                if available, and "slow" will always use the slow tokenizer.
            seed: The seed to initialize the random number generator for sampling.
            devices: The devices to run the model. It can be a single device or a list of devices.
                Each device can be either "npu:X" or "npu:X:*" where X is a specific device index.
                If not given, devices saved in the artifacts will be used.
            cache_dir: The cache directory for all generated files for this LLM instance.
                When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
            backend: The backend implementation to run forward() of a model for the LLM.
                The default is LLMBackend.TORCH_PIPELINE_RUNNER.
            paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store. This argument must be given
                if model uses paged attention.
            scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
                that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler.
            packing_type: Packing algorithm. Possible values are "IDENTITY" only for now
            skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
                the pipelines for other purposes than running them with the engine.
        """

        if not os.path.exists(f"{path}/ready"):
            raise ValueError("This artifacts is not valid.")

        # Load configs
        generator_config = GeneratorConfig.load(f"{path}/generator_config.json")
        with open(f"{path}/model_metadata.json", "r") as fp:
            model_metadata = ModelMetadata.model_validate_json(fp.read())
        with open(f"{path}/model_rewriting_config.json") as fp:
            model_rewriting_config = ModelRewritingConfig.model_validate_json(fp.read())
        with open(f"{path}/parallel_config.json") as fp:
            parallel_config = ParallelConfig.model_validate_json(fp.read())
        with open(f"{path}/other_config.json") as fp:
            other_configs = json.load(fp)

        if not bucket_config:
            prefill_buckets = [
                (bucket.batch_size, bucket.attention_size)
                for bucket in generator_config.prefill_buckets
            ]
            decode_buckets = [
                (bucket.batch_size, bucket.attention_size)
                for bucket in generator_config.decode_buckets
            ]
            bucket_config = ManualBucketConfig(prefill_buckets, decode_buckets)

        if not isinstance(bucket_config, BucketConfig):
            raise ValueError("`bucket_config` must be an instance of BucketConfig.")

        # To ensure not to filter out any buckets.
        max_seq_len_to_capture = sys.maxsize

        try_from_lir = os.environ.get("LLM_ENGINE_ARTIFACTS_TRY_FROM_LIR", "0") == "1"
        try_from_dfg = os.environ.get("LLM_ENGINE_ARTIFACTS_TRY_FROM_DFG", "0") == "1"

        # Load all saved pipelines
        pipelines = cls.__load_pipelines(
            path,
            try_from_lir=try_from_lir,
            try_from_dfg=try_from_dfg,
            cache_dir=cache_dir,
        )

        paged_attention_num_blocks = paged_attention_num_blocks or getattr(
            generator_config.paged_attention_config, "num_blocks", None
        )
        paged_attention_block_size = getattr(
            generator_config.paged_attention_config, "block_size", 1
        )
        comp_supertask_kind = other_configs["comp_supertask_kind"]

        if devices is None:
            devices = other_configs.get("devices")
            if devices is None and not os.environ.get(
                "DISABLE_LLM_ENGINE_ARTIFACTS_STRICT_LOAD", False
            ):
                raise ValueError(
                    "Saved devices info is not found in the artifacts. Please provide devices explicitly or set `DISABLE_LLM_ENGINE_ARTIFACTS_STRICT_LOAD=1` to use all available devices."
                )
            devices = [Device(device) for device in devices]

        return cls(
            model_metadata.pretrained_id,
            task_type=model_metadata.task_type,
            llm_config=model_metadata.llm_config,
            config=model_metadata.hf_configs,
            bucket_config=bucket_config,
            max_seq_len_to_capture=max_seq_len_to_capture,
            tensor_parallel_size=parallel_config.tensor_parallel_size,
            pipeline_parallel_size=parallel_config.pipeline_parallel_size,
            data_parallel_size=data_parallel_size,
            tokenizer=tokenizer,
            tokenizer_mode=tokenizer_mode,
            seed=seed,
            devices=devices,
            do_decompositions_for_model_rewrite=model_rewriting_config.do_decompositions_for_model_rewrite,
            comp_supertask_kind=comp_supertask_kind,
            cache_dir=cache_dir,
            backend=backend,
            use_blockwise_compile=model_rewriting_config.use_blockwise_compile,
            num_blocks_per_supertask=model_rewriting_config.num_blocks_per_supertask,
            embed_all_constants_into_graph=model_rewriting_config.embed_all_constants_into_graph,
            paged_attention_num_blocks=paged_attention_num_blocks,
            paged_attention_block_size=paged_attention_block_size,
            kv_cache_sharing_across_beams_config=generator_config.kv_cache_sharing_across_beams_config,
            scheduler_config=scheduler_config,
            packing_type=packing_type,
            skip_engine=skip_engine,
            _cleanup=_cleanup,
            _pipelines=pipelines,
            **kwargs,
        )

    @staticmethod
    def __load_pipelines(
        path: Union[str, os.PathLike],
        try_from_lir: bool,
        try_from_dfg: bool,
        cache_dir: Optional[os.PathLike] = CACHE_DIR,
    ) -> List[Pipeline]:
        pipelines = []
        bucket_to_pipeline: Dict[Tuple[bool, Bucket], Pipeline] = {}

        for idx in range(len(glob.glob(f"{path}/pipeline.*.json"))):
            pipeline = Pipeline.load(f"{path}/pipeline.{idx}.json")
            bucket_to_pipeline[_get_bucket_from_pipeline_name(pipeline.name)] = pipeline

        for (is_prefill, bucket), pipeline in bucket_to_pipeline.items():
            # if pipeline is None:
            #     mode = "prefill" if is_prefill else "decode"
            #     raise FileNotFoundError(
            #         f"Pipeline for {mode} bucket {bucket} is not found in artifacts path."
            #     )
            # Overrides the devices with the given devices
            # if devices_for_replacement is not None:
            #     if len(pipeline.devices) != len(devices_for_replacement):
            #         raise ValueError(
            #             f"Devices in the artifacts and the given devices are not matched: {len(pipeline.devices)} != {len(devices)}"
            #         )
            #     pipeline.devices = dict(zip(pipeline.devices.keys(), devices))

            blob_to_device: Dict[DataBlobId, Device] = {}
            for _, task in pipeline.supertasks.items():
                if isinstance(task, CompSuperTask) and task.kind == SuperTaskKind.EDF:
                    if task.data_blob is None:
                        continue
                    blob_to_device[task.data_blob] = pipeline.devices[task.device]

            blob_kind = pipeline.get_blob_kind()
            for id, _ in pipeline.blobs.items():
                kind = blob_kind.get(id)
                if kind == SuperTaskKind.FX:
                    with open(f"{path}/{id}.fx", "r") as fp:
                        pipeline.blobs[id] = fp.read()
                elif kind == SuperTaskKind.EDF:
                    try:
                        from furiosa.native_compiler import (  # type: ignore[import]
                            CompiledGraph,
                            compile_from_path,
                        )
                    except ImportError:
                        logger.error("furiosa-native-compiler is required to load EDF format")
                        raise

                    compiler_config_yaml = f"{path}/{id}.config.yaml"
                    device = blob_to_device[id]
                    target_npu = GraphModuleConverter.get_target_npu_from_device(device)
                    pipeline_mode = (
                        PipelineMode.LLM_PREFILL if is_prefill else PipelineMode.LLM_DECODE
                    )

                    # check if:
                    #   - edf file does not exist,
                    #   - try_from_lir is enabled,
                    #   - and lir exists
                    # then, compile lir to edf
                    if (
                        not os.path.exists(f"{path}/{id}.edf")
                        and try_from_lir
                        and os.path.exists(f"{path}/{id}.lir")
                    ):
                        if try_from_dfg:
                            logger.warning(
                                "Both TRY_FROM_LIR and TRY_FROM_DFG are enabled. In this case, TRY_FROM_LIR is prioritized."
                            )
                        compiler_config = try_compiler_config_from_yaml(
                            compiler_config_yaml, pipeline_mode
                        )
                        logger.info(
                            f"Compiling LIR to EDF for {id} with compiler config {compiler_config}"
                        )
                        out = compile_from_path(
                            f"{path}/{id}.lir",
                            target_npu,
                            target_ir="edf",
                            config=compiler_config,
                            dump_tag=id,
                            dump_path=str(path),
                        )
                        contents = CompiledGraph.serialize(out)
                        with open(f"{path}/{id}.edf", "wb") as fp:  # type: ignore[assignment]
                            fp.write(contents)  # type: ignore[arg-type]

                    # check if:
                    #   - edf file does not exist,
                    #   - try_from_dfg is enabled,
                    #   - and dfg exists
                    # then, compile dfg to edf
                    if (
                        not os.path.exists(f"{path}/{id}.edf")
                        and try_from_dfg
                        and os.path.exists(f"{path}/{id}.dfg")
                    ):
                        compiler_config = try_compiler_config_from_yaml(
                            compiler_config_yaml, pipeline_mode
                        )
                        logger.info(
                            f"Compiling DFG to EDF for {id} with compiler config {compiler_config}"
                        )
                        out = compile_from_path(
                            f"{path}/{id}.dfg",
                            target_npu,
                            target_ir="edf",
                            config=compiler_config,
                            dump_tag=id,
                            dump_path=str(path),
                            dump_lir=True,
                        )
                        contents = CompiledGraph.serialize(out)
                        with open(f"{path}/{id}.edf", "wb") as fp:  # type: ignore[assignment]
                            fp.write(contents)  # type: ignore[arg-type]

                    with open(f"{path}/{id}.edf", "rb") as fp:  # type: ignore[assignment]
                        pipeline.blobs[id] = CompiledGraph.deserialize(fp.read(), tag=id)  # type: ignore[arg-type]
                else:
                    raise NotImplementedError(f"SuperTask [{kind}] is not supported to load")

            # Support both cases:
            # 1. param file is located in the artifacts directory
            # 2. param file is located in the global cache directory
            for param_idx, param_file in pipeline.param_files.items():
                # NOTE: param_file.path is already `os.path.basename`d
                path_candidates = (
                    os.path.abspath(f"{path}/{param_file.path}"),
                    os.path.abspath(f"{cache_dir}/param_files/{param_file.path}"),
                )
                for candidate in path_candidates:
                    if os.path.exists(candidate):
                        param_file.path = candidate
                        break
                else:
                    raise FileNotFoundError(
                        f"Param file {param_file.path} is not found in neither artifacts path nor cache directory."
                    )
            pipelines.append(pipeline)

        del bucket_to_pipeline

        return pipelines

    @classmethod
    def compute_prefill_buckets(
        cls,
        preferred_batch_size: int,
        prefill_buckets_num: int,
        prefill_buckets: Optional[Sequence[Tuple[int, int]]],
        max_position_embeddings: int,
    ) -> List[Bucket]:
        if prefill_buckets is not None:
            return [Bucket(batch_size, attn_size) for batch_size, attn_size in prefill_buckets]
        else:
            # Generate the buckets automatically
            percentage = 1.0 / prefill_buckets_num
            interval = max_position_embeddings * percentage
            atten_sizes = [int(interval * i) for i in range(1, prefill_buckets_num + 1)]
            return [Bucket(preferred_batch_size, attn_size) for attn_size in atten_sizes]

    @classmethod
    def compute_decode_buckets(
        cls,
        preferred_batch_size: int,
        decode_buckets_num: int,
        decode_buckets: Optional[Sequence[Tuple[int, int]]],
        max_position_embeddings: int,
    ) -> List[Bucket]:
        if decode_buckets is not None:
            return [Bucket(batch_size, attn_size) for batch_size, attn_size in decode_buckets]
        else:
            # Generate the buckets automatically
            percentage = 1.0 / decode_buckets_num
            interval = max_position_embeddings * percentage
            attn_sizes = [int(interval * i) for i in range(1, decode_buckets_num + 1)]
            return [Bucket(preferred_batch_size, attn_size) for attn_size in attn_sizes]

    @classmethod
    def __verify_buckets(
        cls,
        prefills: Sequence[Bucket],
        decodes: Sequence[Bucket],
        kv_cache_beam_sharing: Optional[KvCacheSharingAcrossBeamsConfig],
    ):
        if kv_cache_beam_sharing is not None:
            for bucket in decodes:
                if bucket.batch_size % kv_cache_beam_sharing.beam_width != 0:
                    raise ValueError(
                        f"decode batch size must be a multiple of beam width, but got {bucket.batch_size} % {kv_cache_beam_sharing.beam_width} != 0"
                    )
                if bucket.attention_size <= kv_cache_beam_sharing.max_new_tokens:
                    raise ValueError(
                        f"decode bucket's attention size must be greater than max_new_tokens, but got {bucket.attention_size} < {kv_cache_beam_sharing.max_new_tokens}"
                    )

    @staticmethod
    def __verify_comp_supertask_kind(kind: str) -> None:
        if kind not in ("fx", "dfg", "edf"):
            raise ValueError(
                f"Unknown comp_supertask_kind: {kind}. Must be either 'fx', 'dfg', or 'edf'."
            )

    @staticmethod
    def __verify_tokenizer_mode(tokenizer_mode: TokenizerModeType) -> None:
        tokenizer_mode_lowered = tokenizer_mode.lower()
        if tokenizer_mode_lowered not in get_args(TokenizerModeType):
            valid_options = ",".join(get_args(TokenizerModeType))
            raise ValueError(
                f"Unknown tokenizer mode: {tokenizer_mode}. Must be one of '{valid_options}'."
            )

    @staticmethod
    def __verify_devices(devices: Sequence[Device]) -> None:
        if len(devices) == 0:
            raise ValueError("No devices are given")
        if not all(dev.kind == devices[0].kind for dev in devices):
            raise ValueError("All devices must be the same kind.")

    @staticmethod
    def __is_generative_model(model_type: Union[str, Type[PreTrainedModel]]) -> bool:
        """Check if the model is a generative model."""
        if isinstance(model_type, str):
            return model_type in _HF_CAUSAL_LM_CLASS_NAMES
        else:
            return model_type.__name__ in _HF_CAUSAL_LM_CLASS_NAMES

    @staticmethod
    def __save_model(
        model: nn.Module,
        path: os.PathLike,
        format: str = "safetensors",
    ):
        if format == "safetensors":
            # FIXME: Use Union operator '|' after Python 3.8 deprecation
            merged_tensors = {**model.state_dict(), **dict(model.named_buffers())}
            write_without_concurrency_issue(merged_tensors, path)
        else:
            raise ValueError(f"Invalid param save format {format}")

    @staticmethod
    @ray.remote
    def __build_pipelines_with_ray(
        buckets: Sequence[
            Tuple[Bucket, bool]
        ],  # First element means whether the bucket is prefill.
        other_args,
    ) -> Tuple[List[Pipeline], List[Pipeline]]:
        (
            model,
            config,
            prefill_pipeline_mode,
            decode_pipeline_mode,
            devices,
            param_file_path,
            cache_dir,
            mppp,
            comp_supertask_kind,
            one_supertask_per_device,
            use_blockwise_compile,
            do_decompositions_for_model_rewrite,
            kv_cache_dtype,
            paged_attention_config,
            sparse_select_version,
            kv_cache_shaing_across_beams_config,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            tmp_dir,
            model_metadata,
            compiler_config_context,
            param_saved_format,
        ) = other_args

        _info_log_for_ray(f"buckets to process: {buckets}")
        prefill_buckets = [bucket for (bucket, is_prefill) in buckets if is_prefill]
        decode_buckets = [bucket for (bucket, is_prefill) in buckets if not is_prefill]

        return LLM.__build_pipelines_inner(
            model,
            config,
            prefill_buckets,
            decode_buckets,
            prefill_pipeline_mode,
            decode_pipeline_mode,
            devices,
            param_file_path,
            cache_dir,
            mppp,
            comp_supertask_kind,
            one_supertask_per_device,
            use_blockwise_compile,
            do_decompositions_for_model_rewrite,
            kv_cache_dtype,
            paged_attention_config,
            sparse_select_version,
            kv_cache_shaing_across_beams_config,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            tmp_dir,
            model_metadata,
            compiler_config_context,
            param_saved_format,
        )

    @staticmethod
    def __build_pipelines_inner(
        model: Union[PreTrainedModel, ModelCreationInfo],
        config: PretrainedConfig,
        prefill_buckets: Sequence[Bucket],
        decode_buckets: Sequence[Bucket],
        prefill_pipeline_mode: PipelineMode,
        decode_pipeline_mode: PipelineMode,
        devices: Sequence[Device],
        param_file_path: os.PathLike,
        cache_dir: Optional[Path],
        mppp: Mppp,
        comp_supertask_kind: SuperTaskKind,
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        kv_cache_dtype: Optional[torch.dtype],
        paged_attention_config: Optional[PagedAttentionConfig],
        sparse_select_version: str,
        kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        tmp_dir: os.PathLike,
        model_metadata: ModelMetadata,
        # config context: name, beam_size
        compiler_config_context: CompilerConfigContext,
        param_saved_format: str = "safetensors",
    ) -> Tuple[List[Pipeline], List[Pipeline]]:
        prefill_pipelines = []
        decode_pipelines = []

        _info_log_for_ray(f"prefill buckets to process: {prefill_buckets}")
        _info_log_for_ray(f"decode buckets to process: {decode_buckets}")

        if isinstance(model, PreTrainedModel):
            original_model_type = model.original_type
        else:
            assert isinstance(model, ModelCreationInfo)
            original_model_type = model.metadata.get_optimized_cls()

        if param_saved_format == "safetensors":
            param_saved_format_ = ParamfileFormat.SAFETENSORS
        elif param_saved_format == "pt":
            param_saved_format_ = ParamfileFormat.TORCHSAVE
        else:
            raise ValueError(f"Invalid param saved format: {param_saved_format}")

        is_beam_search_kv_cache_sharing_model = (
            model_metadata.is_beam_search_kv_cache_sharing_model()
        )
        is_quantized = model_metadata.is_quantized
        pipeline_builder = PipelineBuilder(
            model,
            config,
            tmp_dir,
            is_beam_search_kv_cache_sharing_model=is_beam_search_kv_cache_sharing_model,
        )

        buckets = [(b, True) for b in prefill_buckets] + [(b, False) for b in decode_buckets]
        is_packed_optimized = model_metadata.optimize_options.optimize_packed
        compact_causal_mask_for_bert = model_metadata.is_compact_causal_mask_for_bert()
        use_causal_mask_for_prefill = model_metadata.optimize_options.causal_mask_free_decoding

        for example_input, (bucket, is_prefill) in zip(
            LLM.__generate_input_samples(
                config,
                buckets,
                kv_cache_dtype,
                paged_attention_config,
                kv_cache_shaing_across_beams_config,
                is_packed_optimized,
                compact_causal_mask_for_bert,
                use_causal_mask_for_prefill,
                is_quantized=is_quantized,
            ),
            buckets,
        ):
            mode = "prefill" if is_prefill else "decode"

            padding_block_idx = (
                paged_attention_config.padding_block_idx
                if paged_attention_config is not None
                else None
            )

            model_name = (
                f"Quantized_{original_model_type.__module__}.{original_model_type.__name__}"
                if is_quantized
                else f"{original_model_type.__module__}.{original_model_type.__name__}"
            )

            # Please reflect the implementation of PipelineName in furiosa-llm-tests/src/e2e_base.rs
            pipeline_name = f"{model_name}-{mode}-b{bucket.batch_size}-attn{bucket.attention_size}"
            _info_log_for_ray(f"Generating pipeline {pipeline_name}")
            start = time()
            compiler_config_context = copy.deepcopy(compiler_config_context)
            compiler_config_context.phase = (
                prefill_pipeline_mode if is_prefill else decode_pipeline_mode
            )
            compiler_config_context.bucket = bucket
            pipeline = pipeline_builder.build(
                pipeline_name,
                devices,
                (),
                example_input,
                mppp,
                ParamFileInfo(os.fspath(param_file_path), param_saved_format_),
                compiler_config_context,
                comp_supertask_kind,
                cache_dir=cache_dir,
                one_supertask_per_device=one_supertask_per_device,
                use_blockwise_compile=use_blockwise_compile,
                do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
                padding_block_idx=padding_block_idx,
                sparse_select_version=sparse_select_version,
                embed_all_constants_into_graph=embed_all_constants_into_graph,
                num_blocks_per_supertask=num_blocks_per_supertask,
            )
            _info_log_for_ray(
                f"Finished pipeline generation {pipeline_name}, elapsed: {time() - start:.2f}s"
            )
            if is_prefill:
                prefill_pipelines.append(pipeline)
            else:
                decode_pipelines.append(pipeline)
        return prefill_pipelines, decode_pipelines

    @staticmethod
    def __build_fx_pipelines_parallel(
        model: Union[PreTrainedModel, ModelCreationInfo],
        config: PretrainedConfig,
        prefill_buckets: Sequence[Bucket],
        decode_buckets: Sequence[Bucket],
        prefill_pipeline_mode: PipelineMode,
        decode_pipeline_mode: PipelineMode,
        devices: Sequence[Device],
        param_file_path: os.PathLike,
        cache_dir: Optional[Path],
        mppp: Mppp,
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        kv_cache_dtype: Optional[torch.dtype],
        paged_attention_config: Optional[PagedAttentionConfig],
        sparse_select_version: str,
        kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        tmp_dir: os.PathLike,
        model_metadata: ModelMetadata,
        num_workers: int,
        compiler_config_context: CompilerConfigContext,
        param_saved_format: str = "safetensors",
    ):
        assert num_workers > 1

        buckets = [(bucket, True) for bucket in prefill_buckets] + [
            (bucket, False) for bucket in decode_buckets
        ]

        tasks: List[List[Tuple[Bucket, bool]]] = [list() for _ in range(num_workers)]
        div, remain = divmod(len(buckets), num_workers)
        num_tasks = [div] * num_workers
        for i in range(remain):
            num_tasks[i] += 1

        for i, task in enumerate(tasks):
            while len(task) < num_tasks[i]:
                task.append(buckets.pop(0))
        assert len(buckets) == 0
        assert len(tasks) == num_workers
        assert all(len(task) == num_tasks[i] for i, task in enumerate(tasks))

        common_args = ray.put(
            (
                model,
                config,
                prefill_pipeline_mode,
                decode_pipeline_mode,
                devices,
                param_file_path,
                cache_dir,
                mppp,
                SuperTaskKind.FX,  # Always change this to FX becauase we don't want workers to do compilation.
                one_supertask_per_device,
                use_blockwise_compile,
                do_decompositions_for_model_rewrite,
                kv_cache_dtype,
                paged_attention_config,
                sparse_select_version,
                kv_cache_shaing_across_beams_config,
                embed_all_constants_into_graph,
                num_blocks_per_supertask,
                tmp_dir,
                model_metadata,
                compiler_config_context,
                param_saved_format,
            )
        )
        pipelines_remote = [
            LLM.__build_pipelines_with_ray.remote(
                task,
                common_args,
            )
            for task in tasks[1:]
        ]

        prefill_buckets = [bucket for bucket, is_prefill in tasks[0] if is_prefill]
        decode_buckets = [bucket for bucket, is_prefill in tasks[0] if not is_prefill]

        prefill_pipelines_local, decode_pipelines_local = LLM.__build_pipelines_inner(
            model,
            config,
            prefill_buckets,
            decode_buckets,
            prefill_pipeline_mode,
            decode_pipeline_mode,
            devices,
            param_file_path,
            cache_dir,
            mppp,
            SuperTaskKind.FX,
            one_supertask_per_device,
            use_blockwise_compile,
            do_decompositions_for_model_rewrite,
            kv_cache_dtype,
            paged_attention_config,
            sparse_select_version,
            kv_cache_shaing_across_beams_config,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            tmp_dir,
            model_metadata,
            compiler_config_context,
            param_saved_format,
        )

        pipelines_remote = ray.get(pipelines_remote)

        prefill_pipelines_remote: List[Pipeline] = [  # type: ignore
            prefill_pipeline
            for (prefill_pipelines, _) in pipelines_remote
            for prefill_pipeline in prefill_pipelines  # type: ignore
        ]
        prefill_buckets_remote = [
            bucket for task in tasks[1:] for (bucket, is_prefill) in task if is_prefill
        ]
        decode_pipelines_remote: List[Pipeline] = [  # type: ignore
            decode_pipeline
            for (_, decode_pipelines) in pipelines_remote
            for decode_pipeline in decode_pipelines  # type: ignore
        ]
        decode_buckets_remote = [
            bucket for task in tasks[1:] for (bucket, is_prefill) in task if not is_prefill
        ]

        assert len(prefill_pipelines_remote) == len(prefill_buckets_remote)
        assert len(decode_pipelines_remote) == len(decode_buckets_remote)

        prefill_pipelines = prefill_pipelines_local + prefill_pipelines_remote
        decode_pipelines = decode_pipelines_local + decode_pipelines_remote
        return prefill_pipelines, decode_pipelines

    # FIXME: move parallel building logic into PipelineBuilder,
    @staticmethod
    def __build_pipelines(
        model: Union[PreTrainedModel, ModelCreationInfo],
        config: PretrainedConfig,
        prefill_buckets: Sequence[Bucket],
        decode_buckets: Sequence[Bucket],
        devices: Sequence[Device],
        param_file_path: Optional[os.PathLike],
        cache_dir: Optional[Path],
        backend: LLMBackend,
        mppp: Mppp,
        comp_supertask_kind: SuperTaskKind,
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        kv_cache_dtype: Optional[torch.dtype],
        paged_attention_config: Optional[PagedAttentionConfig],
        sparse_select_version: str,
        kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
        tmp_dir: Optional[os.PathLike],
        model_metadata: ModelMetadata,
        # current context: model_qname, beam_size
        compiler_config_context: CompilerConfigContext,
        num_pipeline_builder_workers: int,
        num_compile_workers: int,
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        is_generative_model: bool,
        param_saved_format: str = "safetensors",
        **kwargs,
    ) -> List[Pipeline]:
        if backend.is_parallelism_supported():
            prefill_pipeline_mode = (
                PipelineMode.LLM_PREFILL if is_generative_model else PipelineMode.UNKNOWN
            )
            decode_pipeline_mode = (
                PipelineMode.LLM_DECODE if is_generative_model else PipelineMode.UNKNOWN
            )

            assert (
                param_file_path is not None
            ), "parameter saved file must be given when using pipeline"
            assert tmp_dir is not None

            num_ray_workers = max(num_pipeline_builder_workers, num_compile_workers)
            if num_ray_workers > 1:
                ray.init(num_cpus=num_ray_workers - 1)

            try:
                if num_pipeline_builder_workers == 1 and num_compile_workers == 1:
                    # no parallelism at all.
                    # In this case, compilation occurs during pipeline building.
                    prefill_pipelines, decode_pipelines = LLM.__build_pipelines_inner(
                        model,
                        config,
                        prefill_buckets,
                        decode_buckets,
                        prefill_pipeline_mode,
                        decode_pipeline_mode,
                        devices,
                        param_file_path,
                        cache_dir,
                        mppp,
                        comp_supertask_kind,
                        one_supertask_per_device,
                        use_blockwise_compile,
                        do_decompositions_for_model_rewrite,
                        kv_cache_dtype,
                        paged_attention_config,
                        sparse_select_version,
                        kv_cache_shaing_across_beams_config,
                        embed_all_constants_into_graph,
                        num_blocks_per_supertask,
                        tmp_dir,
                        model_metadata,
                        compiler_config_context,
                        param_saved_format,
                    )
                    return prefill_pipelines + decode_pipelines
                else:
                    if num_pipeline_builder_workers == 1:
                        prefill_pipelines, decode_pipelines = LLM.__build_pipelines_inner(
                            model,
                            config,
                            prefill_buckets,
                            decode_buckets,
                            prefill_pipeline_mode,
                            decode_pipeline_mode,
                            devices,
                            param_file_path,
                            cache_dir,
                            mppp,
                            SuperTaskKind.FX,
                            one_supertask_per_device,
                            use_blockwise_compile,
                            do_decompositions_for_model_rewrite,
                            kv_cache_dtype,
                            paged_attention_config,
                            sparse_select_version,
                            kv_cache_shaing_across_beams_config,
                            embed_all_constants_into_graph,
                            num_blocks_per_supertask,
                            tmp_dir,
                            model_metadata,
                            compiler_config_context,
                            param_saved_format,
                        )
                    else:
                        # parallelize_pipeline_building
                        prefill_pipelines, decode_pipelines = LLM.__build_fx_pipelines_parallel(
                            model,
                            config,
                            prefill_buckets,
                            decode_buckets,
                            prefill_pipeline_mode,
                            decode_pipeline_mode,
                            devices,
                            param_file_path,
                            cache_dir,
                            mppp,
                            one_supertask_per_device,
                            use_blockwise_compile,
                            do_decompositions_for_model_rewrite,
                            kv_cache_dtype,
                            paged_attention_config,
                            sparse_select_version,
                            kv_cache_shaing_across_beams_config,
                            embed_all_constants_into_graph,
                            num_blocks_per_supertask,
                            tmp_dir,
                            model_metadata,
                            num_pipeline_builder_workers,
                            compiler_config_context,
                            param_saved_format,
                        )

                    if comp_supertask_kind is SuperTaskKind.FX:
                        return prefill_pipelines + decode_pipelines
                    else:
                        return LLM._compile_supertasks_in_pipelines(
                            prefill_pipelines,
                            prefill_buckets,
                            decode_pipelines,
                            decode_buckets,
                            prefill_pipeline_mode,
                            decode_pipeline_mode,
                            comp_supertask_kind.to_ir_kind(),
                            num_compile_workers,
                            compiler_config_context,
                        )
            finally:
                ray.shutdown()
        else:
            raise ValueError(f"unsupported backend: {backend}")

    @staticmethod
    def _compile_supertasks_in_pipelines(
        prefill_pipelines: Sequence[Pipeline],
        prefill_buckets: Sequence[Bucket],
        decode_pipelines: Sequence[Pipeline],
        decode_buckets: Sequence[Bucket],
        prefill_pipeline_mode: PipelineMode,
        decode_pipeline_mode: PipelineMode,
        target_ir: str,
        num_workers: int,
        compiler_config_context: CompilerConfigContext,
    ) -> List[Pipeline]:
        assert len(prefill_pipelines) == len(prefill_buckets)
        assert len(decode_pipelines) == len(decode_buckets)

        def get_updated_compiler_config_context(
            bucket: Bucket, pipeline_mode: PipelineMode
        ) -> CompilerConfigContext:
            new_context = copy.deepcopy(compiler_config_context)
            new_context.phase = pipeline_mode
            new_context.bucket = bucket
            return new_context

        if num_workers == 1:
            for prefill_pipeline, prefill_bucket in zip(prefill_pipelines, prefill_buckets):
                _compile_supertasks_in_pipeline(
                    prefill_pipeline,
                    target_ir,
                    get_updated_compiler_config_context(prefill_bucket, prefill_pipeline_mode),
                )
            for decode_pipeline, decode_bucket in zip(decode_pipelines, decode_buckets):
                _compile_supertasks_in_pipeline(
                    decode_pipeline,
                    target_ir,
                    get_updated_compiler_config_context(decode_bucket, decode_pipeline_mode),
                )
            return [*prefill_pipelines, *decode_pipelines]
        else:
            assert num_workers > 1

            pipelines = [
                *[
                    (
                        get_updated_compiler_config_context(prefill_bucket, prefill_pipeline_mode),
                        prefill_pipeline,
                    )
                    for prefill_pipeline, prefill_bucket in zip_equal(
                        prefill_pipelines, prefill_buckets
                    )
                ],
                *[
                    (
                        get_updated_compiler_config_context(decode_bucket, decode_pipeline_mode),
                        decode_pipeline,
                    )
                    for decode_pipeline, decode_bucket in zip_equal(
                        decode_pipelines, decode_buckets
                    )
                ],
            ]

            share, remainder = divmod(len(pipelines), num_workers)

            remote_pipelines = [
                LLM._compile_supertasks_with_ray.remote(
                    pipelines[
                        worker_idx * share
                        + min(worker_idx, remainder) : (worker_idx + 1) * share
                        + min(worker_idx + 1, remainder)
                    ],
                    target_ir,
                )
                for worker_idx in range(1, num_workers)
            ]

            local_pipelines = LLM._compile_supertasks_in_pipelines_inner(
                pipelines[: share + min(1, remainder)], target_ir
            )
            remote_pipelines = sum(ray.get(remote_pipelines), [])

            # Deserialize serialized compile result if any.
            for pipeline in remote_pipelines:
                assert isinstance(pipeline, Pipeline)
                for task in pipeline.supertasks.values():
                    if not isinstance(task, CompSuperTask) or task.kind == SuperTaskKind.FX:
                        continue
                    try:
                        from furiosa.native_compiler import CompiledGraph  # type: ignore[import]
                    except ImportError:
                        logger.error("furiosa-native-compiler is required to load EDF format")
                        raise

                    if task.data is not None:
                        if isinstance(task.data, bytes):
                            task.data = CompiledGraph.deserialize(task.data, tag="")
                    else:
                        assert task.data_blob is not None
                        data = pipeline.blobs[task.data_blob]  # type: ignore[attr-defined]
                        if isinstance(data, bytes):
                            pipeline.blobs[task.data_blob] = CompiledGraph.deserialize(  # type: ignore[assignment, arg-type, attr-defined]
                                data, tag=task.data_blob
                            )

            return local_pipelines + remote_pipelines  # type: ignore

    @staticmethod
    @ray.remote
    def _compile_supertasks_with_ray(
        pipelines: List[Tuple[CompilerConfigContext, Pipeline]], target_ir: str
    ) -> List[Pipeline]:
        return LLM._compile_supertasks_in_pipelines_inner(
            pipelines, target_ir, serialize_compiled_graphs=True
        )

    @staticmethod
    def _compile_supertasks_in_pipelines_inner(
        pipelines: List[Tuple[CompilerConfigContext, Pipeline]],
        target_ir: str,
        serialize_compiled_graphs: bool = False,
    ) -> List[Pipeline]:
        for compiler_config_context, pipeline in pipelines:
            start = time()
            _info_log_for_ray(f"Compiling supertasks in {pipeline.name}.")
            _compile_supertasks_in_pipeline(
                pipeline,
                target_ir,
                compiler_config_context,
                serialize_compiled_graphs=serialize_compiled_graphs,
            )
            _info_log_for_ray(
                f"Finished compiling supertasks in {pipeline.name}, elapsed: {time() - start:.2f}s."
            )

        return list(map(operator.itemgetter(1), pipelines))

    def _get_buckets(self, bucket_config: BucketConfig) -> Tuple[List[Bucket], List[Bucket]]:
        if isinstance(bucket_config, MinimalBucketConfig):
            buckets_for_prefill = [Bucket(1, bucket_config.max_seq_len)]
            buckets_for_decode = (
                [Bucket(1, bucket_config.max_seq_len)] if self.is_generative_model else []
            )
        elif isinstance(bucket_config, ManualBucketConfig):
            buckets_for_prefill = [Bucket(*bucket) for bucket in bucket_config.prefill_buckets]
            if self.is_generative_model:
                if not bucket_config.decode_buckets:
                    raise ValueError("decode_buckets must be given for generative models.")
                buckets_for_decode = [Bucket(*bucket) for bucket in bucket_config.decode_buckets]
            else:
                if bucket_config.decode_buckets:
                    logger.warning(
                        "decode_buckets will be ignored because the model is not a generative model."
                    )
                buckets_for_decode = []
        else:
            raise ValueError(f"Invalid bucket config: {bucket_config}")
        return buckets_for_prefill, buckets_for_decode

    def _get_default_llm_config_from_pretrained_id(self, pretrained_id: str) -> LLMConfig:
        model_cls = get_model_cls_from_pretrained_id(pretrained_id)
        if model_cls is transformers.GPTJForCausalLM:
            return LLMConfig(  # gptj Optimized packed rope model (M3)
                optimization_config=OptimizationConfig(
                    attention_type=AttentionType.PAGED_ATTENTION,
                    optimize_rope=True,
                    optimize_packed=True,
                    causal_mask_free_decoding=True,
                ),
            )
        elif model_cls is transformers.BertForQuestionAnswering:
            return LLMConfig(  # bert mlperf model
                optimization_config=OptimizationConfig(
                    use_unsplit_packed=True,
                    use_rngd_gelu=True,
                ),
            )
        elif model_cls is transformers.LlamaForCausalLM:
            return LLMConfig(  # Llama MLPerf slice model
                optimization_config=OptimizationConfig(
                    attention_type=AttentionType.PAGED_ATTENTION,
                    optimize_rope=True,
                    optimize_packed=True,
                    causal_mask_free_decoding=True,
                    calculate_logit_only_for_last_token=True,
                )
            )
        else:
            raise NotImplementedError(f"Unsupported model architecture: {model_cls}")

    def _load_available_buckets_from_artifacts(
        self, artifacts_path: Union[str, os.PathLike]
    ) -> Tuple[Sequence[Tuple[int, int]], Optional[Sequence[Tuple[int, int]]]]:
        prefill_buckets = []
        decode_buckets = []
        for idx in range(len(glob.glob(f"{artifacts_path}/pipeline.*.json"))):
            pipeline = Pipeline.load(f"{artifacts_path}/pipeline.{idx}.json")
            is_prefill, bucket = _get_bucket_from_pipeline_name(pipeline.name)
            if is_prefill:
                prefill_buckets.append((bucket.batch_size, bucket.attention_size))
            else:
                decode_buckets.append((bucket.batch_size, bucket.attention_size))

        return prefill_buckets, decode_buckets

    def build_all_pipelines(
        self,
        model: ModelCreationInfo,
        devices: Sequence[Device],
        backend: LLMBackend,
        comp_supertask_kind: str,
        use_random_weight: bool,
        qformat_path: Optional[os.PathLike],
        qparam_path: Optional[os.PathLike],
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        do_decompositions_for_model_rewrite: bool,
        kv_cache_dtype: torch.dtype,
        sparse_select_version: str,
        num_pipeline_builder_workers: int,
        num_compile_workers: int,
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        param_file_path: Optional[os.PathLike],
        param_saved_format: str,
        compiler_config_context: CompilerConfigContext,
        cache_dir: Optional[os.PathLike],
        cleanup: bool,
        **kwargs,
    ) -> None:
        # If backend using Pipeline is used, create directory for temporary files.
        tmp_dir_path = None
        if backend.is_parallelism_supported():
            if cleanup:
                self.tmp_dir = tempfile.TemporaryDirectory()
                tmp_dir_path = Path(self.tmp_dir.name)
            else:
                tmp_dir_path = Path(tempfile.mkdtemp())

        # Save model parameters when param file path is not given
        # and pipeline should be constructed.
        if param_file_path is None and backend.is_parallelism_supported():
            if cache_dir is not None and model.is_hashable():
                param_file_cache_dir = Path(cache_dir) / "param_files"
                param_file_path = LLM._get_param_file_with_cache(model, param_file_cache_dir)
            else:
                assert isinstance(tmp_dir_path, Path)
                param_file_path = tmp_dir_path / _PARAM_FILE_NAME
                self._instantiate_and_save_model(
                    use_random_weight,
                    qformat_path,
                    qparam_path,
                    param_file_path,
                )

        cache_dir = None if cache_dir is None else Path(cache_dir)

        # For now, `PipelineParallelismMppp` supports all valid cases because only pipeline parallelism is needed to be expressed within one pipeline.
        mppp = kwargs.pop("mppp", None) or PipelineParallelismMppp()

        # Build Pipelines for first dp subgroup.
        self.pipelines = LLM.__build_pipelines(
            model,
            self.model_config,
            self.generator_config.prefill_buckets,
            self.generator_config.decode_buckets,
            devices,
            param_file_path,
            cache_dir,
            backend,
            mppp,
            SuperTaskKind.from_str(comp_supertask_kind),
            one_supertask_per_device,
            use_blockwise_compile,
            do_decompositions_for_model_rewrite,
            kv_cache_dtype,
            self.generator_config.paged_attention_config,
            sparse_select_version,
            self.generator_config.kv_cache_sharing_across_beams_config,
            tmp_dir_path,
            self.model_metadata,
            compiler_config_context,
            num_pipeline_builder_workers,
            num_compile_workers,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            self.is_generative_model,
            param_saved_format,
            **kwargs,
        )

        if len(self.pipelines) == 0:
            raise ValueError("No pipeline is generated")

    def _save_engine_artifacts(
        self,
        path: Union[str, os.PathLike],
        comp_supertask_kind: str,
        devices: Sequence[Device],
    ):
        import shutil

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for idx, pipeline in enumerate(self.pipelines):
            blobs = {}
            param_files = copy.deepcopy(pipeline.param_files)

            blob_kind = pipeline.get_blob_kind()
            for id, blob in pipeline.blobs.items():
                blobs[id] = blob
                kind = blob_kind.get(id)
                if kind == SuperTaskKind.FX:
                    with open(f"{path}/{id}.fx", "w") as fp:
                        fp.write(blob)
                elif kind == SuperTaskKind.EDF:
                    with open(f"{path}/{id}.edf", "wb") as fp:
                        fp.write(blob.serialize())  # type: ignore[attr-defined]
                else:
                    raise NotImplementedError(f"SuperTask [{kind}] is not supported to save")
                pipeline.blobs[id] = None  # type: ignore[assignment]

            for param_idx, param_file in pipeline.param_files.items():
                filename = os.path.basename(param_file.path)
                new_path = Path(f"{path}/{filename}")
                if not new_path.exists():
                    shutil.copyfile(param_file.path, new_path)
                pipeline.param_files[param_idx].path = filename

            pipeline.export(f"{path}/pipeline.{idx}.json")
            pipeline.blobs = blobs
            pipeline.param_files = param_files

        self.generator_config.export(f"{path}/generator_config.json")
        self.model_config.to_json_file(f"{path}/hf_config.json", False)

        model_metadata_path = f"{path}/model_metadata.json"
        with open(model_metadata_path, "w") as fp:
            fp.write(self.model_metadata.model_dump_json())

        model_rewriting_config_path = f"{path}/model_rewriting_config.json"
        with open(model_rewriting_config_path, "w") as fp:
            fp.write(self.model_rewriting_config.model_dump_json())

        parallel_config_path = f"{path}/parallel_config.json"
        with open(parallel_config_path, "w") as fp:
            fp.write(self.parallel_config.model_dump_json())

        other_config_path = f"{path}/other_config.json"
        with open(other_config_path, "w") as fp:
            fp.write(
                json.dumps(
                    {
                        "comp_supertask_kind": comp_supertask_kind,
                        "devices": tuple(devices),
                    }
                )
            )

        open(f"{path}/ready", "w").close()

    @staticmethod
    def __verify_sampling_params_with_generator_config(
        sampling_params: SamplingParams,
        generator_config: GeneratorConfig,
    ):
        if generator_config.kv_cache_sharing_across_beams_config is not None:
            if not sampling_params.use_beam_search:
                raise ValueError(
                    "`sampling_params.use_beam_search` is not consistent with generator config. The model was configured to use beam search, but `sampling_params.use_beam_search` is False."
                )
            if (
                sampling_params.max_tokens
                > generator_config.kv_cache_sharing_across_beams_config.max_new_tokens
            ):
                raise ValueError(
                    "`sampling_params.max_tokens` is larger than `generator_config.kv_cache_sharing_across_beams_config.max_new_tokens`"
                )
            if (
                sampling_params.best_of
                != generator_config.kv_cache_sharing_across_beams_config.beam_width
            ):
                raise ValueError(
                    "`sampling_params.best_of` is different from beam width specified in `generator_config.kv_cache_sharing_across_beams_config.beam_width`."
                )

    def generate(
        self,
        prompts: Union[str, List[str]],
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[Union[List[int], List[List[int]]]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Union[RequestOutput, List[RequestOutput]]:
        """Generate texts from given prompts and sampling parameters.

        Args:
            prompts: The prompts to generate texts.
            sampling_params: The sampling parameters for generating texts.
            prompt_token_ids: The token ids of the prompts. If not given, the token ids are
                generated from the prompts using the tokenizer.

        Returns:
            A list of `RequestOutput` objects containing the generated
            completions in the same order as the input prompts.
        """

        if not self.is_generative_model:
            raise ValueError("generate API can only be used for generative models.")

        if prompt_token_ids is None:
            if tokenizer_kwargs is None:
                tokenizer_kwargs = {}
            prompt_token_ids = encode_auto(self.tokenizer, prompts, **tokenizer_kwargs)

        LLM.__verify_sampling_params_with_generator_config(sampling_params, self.generator_config)
        native_outputs = self.engine.generate(prompt_token_ids, sampling_params)
        return self._generate_postprocess(native_outputs, prompts, prompt_token_ids)

    async def stream_generate(
        self,
        prompt: str,
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        is_demo: bool = False,
    ) -> AsyncGenerator[str, None]:
        if not self.is_generative_model:
            raise ValueError("generate API can only be used for generative models.")
        if not isinstance(prompt, str):
            raise ValueError("prompt must be a single string.")

        if prompt_token_ids is None:
            if tokenizer_kwargs is None:
                tokenizer_kwargs = {}
            prompt_token_ids = encode_auto(self.tokenizer, prompt, **tokenizer_kwargs)
        LLM.__verify_sampling_params_with_generator_config(sampling_params, self.generator_config)

        # FIXME: LLM.__init__() should take max_tokens to determine the maximum sequence length through bucket generations
        # and use the config value to raise an error.
        if is_demo and len(prompt_token_ids.input_ids) > 1024:  # type: ignore
            raise ValueError("The length of the prompt is larger than 1024 tokens")

        # NOTE: type of engine.stream_generate() is AsyncGenerator[RequestOutput, None]
        token_buffer = []
        request_output: RequestOutput
        async for request_output in self.engine.stream_generate(prompt_token_ids, sampling_params):
            num_decode_trials = STREAMING_MAX_DECODE_TRIAL
            for completion_output in request_output.outputs:
                token_buffer.extend(completion_output.token_ids)
                num_decode_trials = min(num_decode_trials, len(completion_output.token_ids))

            if num_decode_trials == 0:
                continue

            for tokens_to_discard in range(num_decode_trials):
                end_offset = len(token_buffer) - 1 - tokens_to_discard
                new_text = self.tokenizer.decode(
                    token_buffer[: end_offset + 1], skip_special_tokens=True
                )
                if not new_text.endswith("�"):
                    break
            else:
                continue

            token_buffer = token_buffer[end_offset + 1 :]
            yield new_text

        if token_buffer:
            yield self.tokenizer.decode(token_buffer, skip_special_tokens=True)

    def _instantiate_and_save_model(
        self,
        use_random_weight: bool,
        qformat_path: Optional[os.PathLike],
        qparam_path: Optional[os.PathLike],
        path: os.PathLike,
    ) -> None:
        if use_random_weight:
            model_ = self.model_metadata.random_weight_model(
                qformat_path=qformat_path, qparam_path=qparam_path
            )
        else:
            model_ = self.model_metadata.pretrained_model(
                qformat_path=qformat_path, qparam_path=qparam_path
            )
        LLM.__save_model(model_, path)

    def _generate_postprocess(
        self,
        native_outputs,
        prompts: Union[str, List[str]],
        prompt_token_ids: Union[List[int], List[List[int]]],
    ) -> Union[RequestOutput, List[RequestOutput]]:
        skip_special_tokens = isinstance(prompts, list)

        # Convert one prompt and multiple generated sequences into a RequestOutput
        def convert(prompt: str, _prompt_token_ids: List[int], request_output):
            outputs = [
                CompletionOutput(
                    o.index,
                    self.tokenizer.decode(
                        o.token_ids, skip_special_tokens, clean_up_tokenization_spaces=True
                    ),
                    o.token_ids,
                    None,
                )
                for o in request_output.outputs
            ]

            return RequestOutput(
                request_id=uuid.uuid4().__str__(),
                prompt=prompt,
                prompt_token_ids=_prompt_token_ids,
                outputs=outputs,
                finished=True,
            )

        if isinstance(native_outputs, list):
            assert isinstance(prompts, list)
            return [
                convert(req[0], req[1], req[2])
                for req in zip(prompts, prompt_token_ids.input_ids, native_outputs)  # type: ignore
            ]
        else:
            assert isinstance(prompts, str)
            return convert(prompts, prompt_token_ids.input_ids, native_outputs)  # type: ignore

    def bert_forward(
        self,
        prompts: Union[str, List[str]],
        contexts: Union[str, List[str]],
    ) -> Union[RequestOutput, List[RequestOutput]]:
        prompt_token_ids = encode_auto(self.tokenizer, prompts, text_pair=contexts)
        native_outputs = self.engine.bert_forward(prompt_token_ids)
        return self._generate_postprocess(native_outputs, prompts, prompt_token_ids)

    def __del__(self):
        # Remove tmp directory if exists.
        tmp_dir = getattr(self, "tmp_dir", None)
        if tmp_dir is not None:
            tmp_dir.cleanup()

    @staticmethod
    def __generate_input_samples(
        model_config: PretrainedConfig,
        buckets: Sequence[Tuple["Bucket", bool]],
        kv_cache_dtype: Optional[torch.dtype],
        paged_attention_config: Optional[PagedAttentionConfig],
        kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
        is_packed_optimized: bool,
        compact_causal_mask_for_bert: bool,
        use_causal_mask_for_prefill: bool,
        is_quantized: bool,
    ) -> List[Dict[str, Any]]:
        with FakeTensorMode(allow_non_fake_inputs=True):
            return [
                generate_input_sample(
                    model_config,
                    is_prefill,
                    bucket,
                    kv_cache_dtype,
                    paged_attention_config,
                    kv_cache_shaing_across_beams_config,
                    is_packed_optimized,
                    compact_causal_mask_for_bert,
                    use_causal_mask_for_prefill,
                    is_quantized=is_quantized,
                )
                for bucket, is_prefill in buckets
            ]

    @staticmethod
    def __get_gms_for_pipeline(
        pipeline: Pipeline,
        get_input_constants: bool = False,
    ) -> Union[
        Tuple[GraphModule, ...], Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...]
    ]:
        ret: List = []
        gm_cache: Dict[Optional[DataBlobId], GraphModule] = {}

        # Sort supertasks by id to guarantee consistent order.
        sorted_supertasks = (
            supertask
            for _, supertask in sorted(pipeline.supertasks.items(), key=lambda x: int(x[0]))
        )

        for supertask in sorted_supertasks:
            if not isinstance(supertask, CompSuperTask):
                continue

            if supertask.kind != SuperTaskKind.FX:
                raise ValueError("Supertask is not FX graph supertask.")

            param_load_cache: Dict[Any, Any] = {}

            fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

            with fake_mode:
                fake_example_inputs = tuple(
                    torch.zeros(
                        pipeline.tensors[input_].shape,
                        dtype=pipeline.tensors[input_].dtype.to_torch_dtype(),
                    )
                    for input_ in supertask.inputs
                )

            gm = gm_cache.get(supertask.data_blob, None)
            if gm is None:
                if supertask.data is not None:
                    data = supertask.data
                else:
                    assert supertask.data_blob is not None
                    data = pipeline.blobs[supertask.data_blob]

                gm = deserialize_gm(data)
                # NOTE: This Shape propagation is required because tensor meta infomration is lost during serialization. We need to regenerate this.
                ShapeProp(gm).propagate(*fake_example_inputs)
                # preprocess gms for it to be compiled immediately
                gm = preprocess(gm, fake_example_inputs)

                if supertask.data_blob is not None:
                    gm_cache[supertask.data_blob] = cast(GraphModule, gm)

            if get_input_constants:
                # TODO: change this to share same tensor among slices.
                def load_tensor(tensor_name) -> Optional[torch.Tensor]:
                    tensor_info = pipeline.tensors[tensor_name]
                    if isinstance(tensor_info, TensorInfo):
                        # If it's not an input constant tensor (i.e., input tensor not originated from constant tensor),
                        # just return None.
                        return None
                    else:
                        assert isinstance(tensor_info, ParamInfo)
                        param_value = tensor_info.value
                        param_file_info = pipeline.param_files[param_value.param_file]

                        return load_partial_param(
                            param_file_info.path,
                            param_value.name,
                            param_value.placements,
                            param_file_info.format,
                            cache=param_load_cache,
                        ).contiguous()

                example_input = tuple(load_tensor(input_name) for input_name in supertask.inputs)
                ret.append((gm, example_input))
            else:
                ret.append(gm)

        return tuple(ret)

    def _get_splitted_gms(self, get_input_constants: bool = False) -> Dict[
        str,
        Union[
            Tuple[GraphModule, ...],
            Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...],
        ],
    ]:
        """Get sub GraphModules for each pipeline.

        Returns:
            Dict[str, Union[Tuple[GraphModule, ...], Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...],],]:
                Dictionary whose key is the pipeline name and value is the tuple containing ``GraphModule``s (computation supertasks) and some additional information if necessary.
                if ``get_input_constants==False``, each value is just a tuple of ``GraphModule``s in the pipeline.
                Otherwise, each value is a tuple whose element is ``GraphModule`` in the pipeline  and list of input constant tensors,
                which were originally constant tensors, but converted to input. The list of input constant tensors has same length as corresponding ``GraphModule``'s number of inputs
                with each element exactly corresponding to the input of the ``GraphModule`` with same index, but elements with original input tensor indexes are ``None``.
        """
        if not (isinstance(self.pipelines, Sequence) and isinstance(self.pipelines[0], Pipeline)):
            raise ValueError("get_splitted_gms is only supported for parallel backends")

        return {
            pipeline.name: LLM.__get_gms_for_pipeline(
                pipeline, get_input_constants=get_input_constants
            )
            for pipeline in self.pipelines
        }

    @staticmethod
    def __get_kv_cache_dtype_from_qformat_dict(
        qformat_path: os.PathLike, model_metadata: ModelMetadata
    ) -> torch.dtype:
        node_name_format_dict = {
            transformers.LlamaForCausalLM: "model_layers_{}_self_attn_{}_proj",
            transformers.GPTJForCausalLM: "transformer_h_{}_attn_{}_proj",
        }
        with open(qformat_path, "r") as f:
            qformat_dict = yaml.safe_load(f)

        # Formatting makes this ugly.
        # fmt: off
        kv_cache_dtype_set = set()
        for layer_num in range(model_metadata.get_num_hidden_layers()):
            for k_or_v in ("k", "v"):
                for input_or_weight in ("input", "weight"):
                    node_name = node_name_format_dict[model_metadata.model_cls].format(layer_num, k_or_v)
                    dtype = qformat_dict["quantized op list"][node_name][f"quant_desc_{input_or_weight}"]["dtype"]
                    kv_cache_dtype_set.add(dtype)
        # fmt: on

        if len(kv_cache_dtype_set) != 1:
            raise RuntimeError("The dtype of kv_cache must be the same for all the layers.")

        kv_cache_dtype = kv_cache_dtype_set.pop()

        if dtype := STR_TO_TORCH_DTYPE.get(kv_cache_dtype, None):
            return dtype
        else:
            raise RuntimeError(f"Unsupported quantized kv_cache_dtype: {kv_cache_dtype}")

    @staticmethod
    def __get_kv_cache_dtype_from_qformat(
        qformat_path: os.PathLike, model_metadata: ModelMetadata
    ) -> torch.dtype:
        with open(qformat_path, "r") as f:
            metadata_line = f.readline()
        maybe_kvcache_dtype = re.search(r"--kv_dtype \S+\b", metadata_line)
        if maybe_kvcache_dtype is None:
            return LLM.__get_kv_cache_dtype_from_qformat_dict(qformat_path, model_metadata)
        assert maybe_kvcache_dtype is not None, f"Cannot find kv_cache_dtype from '{metadata_line}'"
        kv_cache_dtype = maybe_kvcache_dtype.group().split()[-1]

        if dtype := STR_TO_TORCH_DTYPE.get(kv_cache_dtype, None):
            return dtype
        else:
            raise RuntimeError(f"Unsupported quantized kv_cache_dtype: {kv_cache_dtype}")

    @staticmethod
    def __verify_kv_cache_dtype_with_qformat(
        kv_cache_dtype: torch.dtype, qformat_path: os.PathLike, model_metadata: ModelMetadata
    ) -> None:
        kv_cache_dtype_from_qformat = LLM.__get_kv_cache_dtype_from_qformat(
            qformat_path, model_metadata
        )
        if kv_cache_dtype != kv_cache_dtype_from_qformat:
            raise ValueError(
                f"kv_cache_dtype != qformat's kv_cache dtype: {kv_cache_dtype} != {kv_cache_dtype_from_qformat}"
            )

    @staticmethod
    def _get_param_file_with_cache(model: ModelCreationInfo, cache_dir: os.PathLike) -> Path:
        # Find if cached param file exists.
        model_hash = hash_model(
            model.metadata.get_optimized_cls(),
            model.metadata.config,
            model.get_qparam_qformat_path(),
            model.metadata.pretrained_id,
            model.seed,
            model.random_weight_model,
            {
                "enforce_saved_param_name_ordering": "true",
            },
        )

        os.makedirs(cache_dir, exist_ok=True)

        cached_path = get_cache_path_if_exists(model_hash, "safetensors", cache_dir)
        if cached_path is None:
            # No cached param file exists. Model instantitation is unavoidable.
            param_file_path = Path(cache_dir) / f"params-{model_hash}.safetensors"
            LLM.__save_model(model.instantiate_model(), param_file_path, "safetensors")
            return param_file_path
        else:
            # Cached param file exists. Return it.
            return cached_path

    @cached_property
    def model_max_seq_len(self) -> int:
        possible_keys = [
            # OPT, LLaMA, BERT
            "max_position_embeddings",
            # GPT-2, GPT-J
            "n_positions",
            # MPT
            "max_seq_len",
            # ChatGLM2
            "seq_length",
            # Command-R
            "model_max_length",
            # Others
            "max_sequence_length",
            "max_seq_length",
            "seq_len",
        ]

        for attr_name in possible_keys:
            if hasattr(self.model_config, attr_name):
                model_max_seq_len = getattr(self.model_config, attr_name)
                break
        else:
            # If none of the keys were found in the config, use a default and
            # log a warning.
            default_max_len = 2048
            model_max_seq_len = default_max_len
            logger.warning(
                "The model's config.json does not contain any of the following "
                "keys to determine the original maximum length of the model: "
                "%s. Assuming the model's maximum length is %d.",
                possible_keys,
                default_max_len,
            )
        return model_max_seq_len


def try_compiler_config_from_yaml(path: str, pipeline_mode: PipelineMode):
    if not os.path.exists(path):
        return CompilerConfigContext(model_qname="unknown", phase=pipeline_mode).load_config()
    with open(path, "r") as f:
        return yaml.safe_load(f)
