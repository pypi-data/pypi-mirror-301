from dataclasses import dataclass, field
import os
from typing import ClassVar, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

try:
    import pytest
except ImportError:
    pass
from transformers import set_seed

from furiosa_llm import LLM, SamplingParams
from furiosa_llm.api import KvCacheSharingAcrossBeamsConfig, ManualBucketConfig, SchedulerConfig
from furiosa_llm.models import ModelMetadata
from furiosa_llm.parallelize.config import Device
from furiosa_llm.tokenizer import get_tokenizer

TEST_SEED_VALUE = 42


# Make this struct and furiosa-rt-python/tests/e2e_base.rs consistent
@dataclass
class LLMTestCase:
    name: str
    model_metadata: ModelMetadata
    prompts: List[str]
    sampling_params: SamplingParams
    seed: int = TEST_SEED_VALUE
    devices: str = "cpu:0"
    prefill_buckets: List[Tuple[int, int]] = field(default_factory=list)
    decode_buckets: List[Tuple[int, int]] = field(default_factory=list)
    max_seq_len_to_capture: int = 2048
    tensor_parallel_size: int = 4
    pipeline_parallel_size: int = 1
    data_parallel_size: Optional[int] = None
    validation_model: Optional[ModelMetadata] = (
        None  # For some model, you may need to use a different model for validation.
    )
    num_blocks_per_supertask: int = 1
    paged_attention_num_blocks: Optional[int] = None
    kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None
    qa_context: Optional[List[str]] = None
    scheduler_config: SchedulerConfig = SchedulerConfig(spare_blocks_ratio=0.0)
    compiler_config_overrides: Optional[Mapping] = None
    use_random_weight: bool = False
    device_sets_for_actual_use: Optional[Sequence[Union[str, Sequence[Device]]]] = None
    embed_all_constants_into_graph: bool = False
    num_pipeline_builder_workers: int = int(os.environ.get("NUM_PIPELINE_BUILDER_WORKERS", 1))
    num_compile_workers: int = int(os.environ.get("NUM_COMPILE_WORKERS", 1))
    skip_validation: bool = False

    _BY_NAME: ClassVar[Dict[str, "LLMTestCase"]] = {}

    @classmethod
    def xxfail(cls, reason: str, *args, **kwargs):
        """Marks this test case to be known to fail (xfail) and shouldn't be run by default.
        Use `--runxfail` to run such test cases."""
        return pytest.param(cls(*args, **kwargs), marks=pytest.mark.xfail(reason=reason, run=False))

    def __class_getitem__(cls, name: str) -> "LLMTestCase":
        return cls._BY_NAME[name]

    def __post_init__(self):
        try:
            old = self._BY_NAME[self.name]
        except KeyError:
            self._BY_NAME[self.name] = self
            return

        if self != old:
            raise ValueError(
                f"LLMTestCase {self.name} has an inconsistent value:\n{old!r}\n{self!r}"
            )

    def __str__(self):
        # Use all attributes to generate string representation
        return str(self.__dict__)

    @property
    def test_param_id(self):
        return self.name

    def test_uses_models(self) -> Iterable[ModelMetadata]:
        if self.validation_model is not None:
            return [self.model_metadata, self.validation_model]
        return [self.model_metadata]

    def is_model_available(self) -> bool:
        return self.model_metadata.is_model_available()


def run_furiosa_llm(
    test_case: LLMTestCase,
    **kwargs,
) -> Union[List[str], List[List[str]]]:
    set_seed(test_case.seed)
    llm = prestep_furiosa_llm(test_case, **kwargs)
    request_output = llm.generate(test_case.prompts, test_case.sampling_params)
    return poststep_furiosa_llm(request_output, llm.tokenizer)


def prestep_furiosa_llm(
    test_case: LLMTestCase,
    **kwargs,
) -> LLM:
    # Analyze the LLM parameters from prompts and sampling params
    tokenizer = kwargs.pop("tokenizer", None)
    if not tokenizer:
        tokenizer = get_tokenizer(test_case.model_metadata.pretrained_name, **kwargs)

    qformat_path: Optional[os.PathLike] = None
    qparam_path: Optional[os.PathLike] = None

    # FIXME: Remove this after fixing all rust tests and furiosa-mlperf to call
    # `LLM.from_artifacts` directly when artifacts is presence.
    if artifacts_path := os.environ.get("LLM_ENGINE_ARTIFACTS_PATH"):
        llm = LLM.from_artifacts(
            artifacts_path,
            bucket_config=ManualBucketConfig(
                prefill_buckets=test_case.prefill_buckets, decode_buckets=test_case.decode_buckets
            ),
            data_parallel_size=test_case.data_parallel_size,
            tokenizer=tokenizer,
            seed=test_case.seed,
            devices=test_case.devices,
            paged_attention_num_blocks=test_case.paged_attention_num_blocks,
            scheduler_config=test_case.scheduler_config,
            device_sets_for_actual_use=test_case.device_sets_for_actual_use,
            **kwargs,
        )
    else:
        llm = LLM(
            model=test_case.model_metadata.pretrained_id,
            task_type=test_case.model_metadata.task_type,
            llm_config=test_case.model_metadata.llm_config,
            qformat_path=qformat_path,
            qparam_path=qparam_path,
            config=test_case.model_metadata.hf_configs,
            bucket_config=ManualBucketConfig(
                prefill_buckets=test_case.prefill_buckets, decode_buckets=test_case.decode_buckets
            ),
            max_seq_len_to_capture=test_case.max_seq_len_to_capture,
            tensor_parallel_size=test_case.tensor_parallel_size,
            pipeline_parallel_size=test_case.pipeline_parallel_size,
            data_parallel_size=test_case.data_parallel_size,
            tokenizer=tokenizer,
            seed=test_case.seed,
            devices=test_case.devices,
            num_blocks_per_supertask=test_case.num_blocks_per_supertask,
            embed_all_constants_into_graph=test_case.embed_all_constants_into_graph,
            paged_attention_num_blocks=test_case.paged_attention_num_blocks,
            kv_cache_sharing_across_beams_config=test_case.kv_cache_sharing_across_beams_config,
            scheduler_config=test_case.scheduler_config,
            compiler_config_overrides=test_case.compiler_config_overrides,
            device_sets_for_actual_use=test_case.device_sets_for_actual_use,
            use_random_weight=test_case.use_random_weight,
            num_pipeline_builder_workers=test_case.num_pipeline_builder_workers,
            num_compile_workers=test_case.num_compile_workers,
            **kwargs,
        )

    return llm


def poststep_furiosa_llm(
    request_output,
    tokenizer,
) -> Union[List[str], List[List[str]]]:
    if not isinstance(request_output, list):
        request_output = [request_output]

    # FIXME: workaround for BPE-based tokenizer that LLaMA uses.
    #  See: https://github.com/furiosa-ai/furiosa-sdk-private/pull/759#issuecomment-1899648400
    return [
        [
            tokenizer.decode(
                req.prompt_token_ids + output.token_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
            for output in req.outputs
        ]
        for req in request_output
    ]
