from contextlib import AbstractContextManager, ExitStack, nullcontext
import copy
from copy import deepcopy
from enum import Enum
import functools
import json
import logging
import os
from pathlib import Path
import sys
from typing import (
    Any,
    ContextManager,
    Dict,
    Final,
    FrozenSet,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
from unittest.mock import patch
import warnings

from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator
import torch
import transformers
from transformers import AutoConfig, PretrainedConfig, PreTrainedModel, set_seed

from .quantized_models import QuantCausalLM, get_quantized_causal_lm
from .utils import enforce_torch_load_with_mmap, replace_layernorm

TEST_SEED_VALUE: Final = 42
# The maximum number of `Model.pretrained_models` kept.
# A custom pytest hook is used to group parametrized tests to work around this limit.
# Note that this should be at least 2 because quantized models recursively load base models!
PRETRAINED_MODEL_CACHE_SIZE: Final = 2
FURIOSA_LLM_PACKAGE_PATH: Final = Path(__file__).parent.parent
TINY_GPTJ_CONFIG: Final[Dict[str, Any]] = {
    "n_embd": 32,
    "rotary_dim": 2,
    "n_inner": 1,
}


MLPERF_BERT_LARGE_PRETRAINED_ID: Final[str] = "furiosa-ai/mlperf-bert-large"
BERT_SMALL_SQUAD_PRETRAINED_ID: Final[str] = "anas-awadalla/bert-small-pretrained-finetuned-squad"
BERT_BASE_SQUAD_PRETRINED_ID: Final[str] = "csarron/bert-base-uncased-squad-v1"
BERT_LARGE_SQUAD_PRETRAINED_ID: Final[str] = (
    "google-bert/bert-large-uncased-whole-word-masking-finetuned-squad"
)

GPT_2_PRETRAINED_ID: Final[str] = "gpt2"
GPT_2_SMALL_PRETRAINED_ID: Final[str] = "openai-community/gpt2"
GPT_2_MEDIUM_PRETRAINED_ID: Final[str] = "openai-community/gpt2-medium"
GPT_2_LARGE_PRETRAINED_ID: Final[str] = "openai-community/gpt2-large"
GPT_2_XLARGE_PRETRAINED_ID: Final[str] = "openai-community/gpt2-xl"

GPT_NEO_PRETRAINED_ID: Final[str] = "EleutherAI/gpt-neo-125m"

GPT_J_PRETRAINED_ID: Final[str] = "EleutherAI/gpt-j-6B"
MLPERF_GPTJ_PRETRAINED_ID: Final[str] = "furiosa-ai/mlperf-gpt-j-6b"

LLAMA_7B_PRETRAINED_ID: Final[str] = "huggyllama/llama-7b"
CODE_LLAMA_7B_PRETRAINED_ID: Final[str] = "meta-llama/CodeLlama-7b-Instruct-hf"

LLAMA2_7B_PRETRAINED_ID: Final[str] = "meta-llama/Llama-2-7b-hf"
LLAMA2_70B_CHAT_PRETRAINED_ID: Final[str] = "meta-llama/Llama-2-70b-chat-hf"
VICUNA_7B_PRETRAINED_ID: Final[str] = "lmsys/vicuna-7b-v1.5"

LLAMA3_1_8B_PRERTRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-8B"
LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-8B-Instruct"
LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-70B-Instruct"

ROBERTA_BASE_SQUAD_PRETRAINED_ID: Final[str] = "csarron/roberta-base-squad-v1"
ROBERTA_LARGE_SQUAD_PRETRAINED_ID: Final[str] = "csarron/roberta-large-squad-v1"


MODEL_CLS_TO_QUANT_DIR_NAME: Final[Dict[Type[PreTrainedModel], str]] = {
    transformers.GPTJForCausalLM: "GPT-J",
    transformers.BertForQuestionAnswering: "BERT-large",
}

TTA_MODEL_PRETRAINED_IDS: Final[Set[str]] = {
    BERT_SMALL_SQUAD_PRETRAINED_ID,
    BERT_BASE_SQUAD_PRETRINED_ID,
    BERT_LARGE_SQUAD_PRETRAINED_ID,
    GPT_J_PRETRAINED_ID,
    GPT_2_SMALL_PRETRAINED_ID,
    GPT_2_MEDIUM_PRETRAINED_ID,
    GPT_2_LARGE_PRETRAINED_ID,
    GPT_2_XLARGE_PRETRAINED_ID,
    CODE_LLAMA_7B_PRETRAINED_ID,
    LLAMA2_7B_PRETRAINED_ID,
    LLAMA3_1_8B_PRERTRAINED_ID,
    VICUNA_7B_PRETRAINED_ID,
    ROBERTA_BASE_SQUAD_PRETRAINED_ID,
    ROBERTA_LARGE_SQUAD_PRETRAINED_ID,
}

MODEL_CONFIG_ROOT_DIR = Path(__file__).with_name("model_configs")

with open(MODEL_CONFIG_ROOT_DIR / "LLaMA3.1-8B.json") as f:
    LLAMA3_1_8B_CONFIG = json.load(f)

with open(MODEL_CONFIG_ROOT_DIR / "LLaMA3.1-70B.json") as f:
    LLAMA3_1_70B_CONFIG = json.load(f)

logger = logging.getLogger(__name__)


class DummyModel(torch.nn.Module):
    def __init__(self, batch_size: int = 1):
        super(DummyModel, self).__init__()
        self.linear1 = torch.nn.Linear(16, batch_size)

    def forward(self, x):
        return self.linear1(x)


class QDtype(str, Enum):
    INT8 = "int8"
    FP8 = "fp8"
    BF16 = "bf16"

    def bits(self) -> int:
        if self in (QDtype.INT8, QDtype.FP8):
            return 8
        elif self == QDtype.BF16:
            return 16
        else:
            raise ValueError(f"{self}.bits() is not supported")

    def to_torch_dtype(self) -> torch.dtype:
        if self is QDtype.INT8:
            return torch.int8
        elif self is QDtype.FP8:
            return torch.int8
        elif self is QDtype.BF16:
            return torch.bfloat16
        else:
            raise ValueError(f"{self} has no corresponding torch dtype")

    def suffix(self):
        if self is QDtype.INT8:
            return "8"
        elif self is QDtype.FP8:
            return "8f"
        elif self is QDtype.BF16:
            return "16bf"
        else:
            raise ValueError(f"{self} is not supported")


@functools.total_ordering
class QuantizationConfig(BaseModel):
    weight: QDtype
    activation: QDtype
    kv_cache: Optional[QDtype]

    def __hash__(self) -> int:
        return hash(repr(self))

    @classmethod
    def w_i8_a_i8_kv_i8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.INT8, activation=QDtype.INT8, kv_cache=QDtype.INT8)

    @classmethod
    def w_i8_a_i8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.INT8, activation=QDtype.INT8, kv_cache=None)

    @classmethod
    def w_f8_a_f8_kv_f8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.FP8, activation=QDtype.FP8, kv_cache=QDtype.FP8)

    @classmethod
    def w_f8_a_f8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.FP8, activation=QDtype.FP8, kv_cache=None)

    @field_serializer('weight', 'activation', 'kv_cache')
    def serialize(self, dtype: Optional[QDtype]) -> Optional[str]:
        return dtype.value if dtype else None

    @field_validator('weight', 'activation', 'kv_cache', mode="before")
    @classmethod
    def deserialize(cls, dtype: Union[None, str, QDtype]) -> Optional[QDtype]:
        if dtype is None:
            return None
        if isinstance(dtype, QDtype):
            return dtype
        elif isinstance(dtype, str):
            return QDtype(dtype)
        raise ValueError(f"Invalid dtype: {dtype!r}")

    def __str__(self) -> str:
        return "W{}A{}{}".format(
            self.weight.suffix(),
            self.activation.suffix(),
            f"KV{self.kv_cache.suffix()}" if self.kv_cache else "",
        )

    def __lt__(self, other):
        return str(self) < str(other)


@functools.total_ordering
class AttentionType(Enum):
    VANILLA = "VANILLA"
    PAGED_ATTENTION = "PAGED_ATTENTION"
    # preallocate memory space for kv cache, return in-place updated kv cache (concat)
    PREALLOCATION_CONCAT = "PREALLOCATION_CONCAT"

    def __lt__(self, other):
        if not isinstance(other, AttentionType):
            return NotImplemented
        return self.value < other.value


@functools.total_ordering
class OptimizationConfig(BaseModel):
    attention_type: AttentionType = AttentionType.VANILLA
    optimize_rope: bool = False
    optimize_packed: bool = False
    decompose_layernorm: bool = False
    optimize_furiosa: bool = False
    use_unsplit_packed: bool = False
    compact_causal_mask: bool = False
    use_rngd_gelu: bool = False
    causal_mask_free_decoding: bool = False
    kv_cache_sharing_across_beams: bool = False
    inbound_beamsearch_softmax: bool = False
    # https://furiosa-ai.slack.com/archives/C06R68UU9DJ/p1720453142548739
    calculate_logit_only_for_last_token: bool = False

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other):
        return repr(self) < repr(other)

    def get_activated_options(self) -> FrozenSet[str]:
        return frozenset(
            key
            for key, value in self.model_dump().items()
            if value and key not in {"attention_type"}
        )

    def get_all_flags(self) -> FrozenSet[str]:
        return frozenset(key for key in self.model_dump() if key != "attention_type")

    def contains(self, other: "OptimizationConfig") -> bool:
        return self.get_enabled_opts().issuperset(other.get_enabled_opts())

    def get_enabled_opts(self) -> Set[str]:
        return {
            k
            for k, v in self.model_dump().items()
            if (k == "attention_type" and v != AttentionType.VANILLA)
            or (k != "attention_type" and v)
        }


# FIXME: there exists a gptj_rope_packed_rngd_gelu model and it differs from mlperf_submission
MODEL_CLS_TO_MLPERF_OPT_CONFIGS = {
    transformers.GPTJForCausalLM: OptimizationConfig(
        attention_type=AttentionType.PAGED_ATTENTION,
        optimize_rope=True,
        optimize_packed=True,
        use_rngd_gelu=True,
        kv_cache_sharing_across_beams=True,
        causal_mask_free_decoding=True,
        inbound_beamsearch_softmax=True,
    ),
    transformers.LlamaForCausalLM: OptimizationConfig(
        attention_type=AttentionType.PAGED_ATTENTION,
        optimize_rope=True,
        optimize_packed=True,
        causal_mask_free_decoding=True,
    ),
    transformers.BertForQuestionAnswering: OptimizationConfig(
        use_unsplit_packed=True,
        use_rngd_gelu=True,
    ),
}


@functools.lru_cache
def get_model_cls_from_pretrained_id(
    pretrained_id: str, task_type: Optional[str] = None
) -> Type[PreTrainedModel]:
    # LLAMA v3 model config cannot be crated from AutoConfig.from_pretrained becasue we are using outdated transformers version.
    if pretrained_id in {
        LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_8B_PRERTRAINED_ID,
    }:
        if task_type and task_type != "text-generation":
            raise NotImplementedError(f"Unsupported task_type for llama3: {task_type}")
        return transformers.LlamaForCausalLM
    model_config = transformers.AutoConfig.from_pretrained(pretrained_id)
    supported_architectures = getattr(model_config, "architectures", [])

    if task_type:
        if task_type == "text-generation":
            model_cls = transformers.MODEL_FOR_CAUSAL_LM_MAPPING.get(type(model_config), None)
        elif task_type == "question-answering":
            model_cls = transformers.MODEL_FOR_QUESTION_ANSWERING_MAPPING.get(
                type(model_config), None
            )
        else:
            raise NotImplementedError(f"Unsupported task_type: {task_type}")

        if model_cls is None:
            raise ValueError(
                f"There's no model architecture for pretrained id {pretrained_id} and task_type {task_type}"
            )
    else:
        if len(supported_architectures) != 1:
            raise ValueError(
                f"Task type not given, but multiple architectures found: {supported_architectures}"
            )
        if not (model_cls := getattr(transformers, supported_architectures[0], None)):
            raise ValueError(
                f"Default model architecture of pretrained id {pretrained_id} is not valid."
            )

    if model_cls.__name__ not in supported_architectures:
        logging.warning(f"Unsupported task type {task_type} for pretrained id {pretrained_id}")

    return model_cls


def get_default_task_type_from_pretrained_id(pretrained_id: str) -> str:
    model_cls = get_model_cls_from_pretrained_id(pretrained_id, None)
    if model_cls in transformers.MODEL_FOR_CAUSAL_LM_MAPPING.values():
        return "text-generation"
    elif model_cls in transformers.MODEL_FOR_QUESTION_ANSWERING_MAPPING.values():
        return "question-answering"
    else:
        raise ValueError(f"cannot set task_type automatically for {model_cls}")


class LLMConfig(BaseModel, frozen=True):
    optimization_config: OptimizationConfig = OptimizationConfig()
    quantization_config: Optional[QuantizationConfig] = None

    def __init__(
        self,
        optimization_config: OptimizationConfig = OptimizationConfig(),
        quantization_config: Optional[QuantizationConfig] = None,
    ):
        super(LLMConfig, self).__init__(
            optimization_config=optimization_config, quantization_config=quantization_config
        )

    def with_quantization_config(self, quantization_config: QuantizationConfig) -> "LLMConfig":
        return LLMConfig(self.optimization_config, quantization_config)

    def with_optimizations(self, opts: Dict[str, Any]) -> "LLMConfig":
        new_dict = self.optimization_config.model_dump()
        new_dict.update(opts)
        new_opt_config = OptimizationConfig(**new_dict)
        return LLMConfig(new_opt_config, self.quantization_config)


class DecomposedLayerNorm(torch.nn.Module):
    def __init__(self, hidden_size, eps=1e-5):
        """
        Decomposed torch.nn.LayerNorm for efficient chip2chip communication by decomposing in more smaller units.
        This is only available for inference.
        """
        super().__init__()
        self.weight = torch.nn.Parameter(torch.ones(hidden_size))
        self.bias = torch.nn.Parameter(torch.zeros(hidden_size))
        self.variance_epsilon = eps
        self.hidden_size = hidden_size

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        mean = hidden_states.mean(-1, keepdim=True)
        pow_mean = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = (
            self.weight
            * (hidden_states - mean)
            * torch.rsqrt(pow_mean - mean.pow(2) + self.variance_epsilon)
            + self.bias
        )

        return hidden_states.to(input_dtype)


@functools.total_ordering
class ModelMetadata(BaseModel):
    pretrained_id: str
    task_type: Optional[str] = None
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    hf_configs: Dict[str, Any] = Field(default_factory=dict)
    # path to load pre-trained model weights (optional)
    model_weight_path: Optional[os.PathLike] = None

    @field_validator("pretrained_id")
    def validate_pretrained_id(cls, value: str) -> str:
        assert value, "pretrained_id must be provided"
        get_model_cls_from_pretrained_id(value)
        return value

    @model_validator(mode='after')
    def validate_model_metadata(self):
        if self.task_type is None:
            self.task_type = get_default_task_type_from_pretrained_id(self.pretrained_id)
        assert self.task_type in transformers.pipelines.SUPPORTED_TASKS, "unsupported task_type"
        return self

    @property
    @functools.lru_cache
    def model_cls(self) -> Type[PreTrainedModel]:
        return get_model_cls_from_pretrained_id(self.pretrained_id, self.task_type)

    @property
    def _is_tiny_gptj(self) -> bool:
        config_without_num_hidden_layers = {
            k: v for k, v in self.hf_configs.items() if k != "num_hidden_layers"
        }

        return (
            self.model_cls == transformers.GPTJForCausalLM
            and config_without_num_hidden_layers == TINY_GPTJ_CONFIG
        )

    @property
    def num_hidden_layers(self) -> int:
        return self.hf_configs["num_hidden_layers"]

    @property
    def attention_type(self) -> AttentionType:
        return self.llm_config.optimization_config.attention_type

    @property
    def optimize_options(self) -> OptimizationConfig:
        return self.llm_config.optimization_config

    @property
    def quantization_config(self) -> Optional[QuantizationConfig]:
        return self.llm_config.quantization_config

    def __init__(
        self,
        pretrained_id: str,
        task_type: Optional[str] = None,
        llm_config: LLMConfig = LLMConfig(),
        hf_configs: Dict = {},
        model_weight_path: Optional[os.PathLike] = None,
    ):
        # This is needed for tokenizer generation. Tokenizer will be created from this information.
        hf_configs["_name_or_path"] = pretrained_id
        super(ModelMetadata, self).__init__(
            pretrained_id=pretrained_id,
            task_type=task_type,
            llm_config=llm_config,
            hf_configs=hf_configs,
            model_weight_path=model_weight_path,
        )
        self.hf_configs.setdefault("num_hidden_layers", self.full_layer_count)

    @classmethod
    def init_with_mlperf_optim_options(
        cls,
        pretrained_id: str,
        quantization_config: Optional[QuantizationConfig] = None,
        hf_configs: Dict = {},
        model_weight_path: Optional[os.PathLike] = None,
    ) -> "ModelMetadata":
        return cls(
            pretrained_id=pretrained_id,
            llm_config=LLMConfig(
                optimization_config=ModelMetadata.get_mlperf_options(
                    get_model_cls_from_pretrained_id(pretrained_id)
                ),
                quantization_config=quantization_config,
            ),
            hf_configs=hf_configs,
            model_weight_path=model_weight_path,
        )

    def with_num_layers(self, num_hidden_layers: int) -> "ModelMetadata":
        return ModelMetadata(
            self.pretrained_id,
            self.task_type,
            self.llm_config,
            {**self.hf_configs, "num_hidden_layers": num_hidden_layers},
            self.model_weight_path,
        )

    def with_quantization_config(self, quantization_config: QuantizationConfig) -> "ModelMetadata":
        return ModelMetadata(
            self.pretrained_id,
            self.task_type,
            self.llm_config.with_quantization_config(quantization_config),
            deepcopy(self.hf_configs),
            self.model_weight_path,
        )

    def with_optimizations(self, opts: Dict[str, Any]) -> "ModelMetadata":
        return ModelMetadata(
            self.pretrained_id,
            self.task_type,
            self.llm_config.with_optimizations(opts),
            deepcopy(self.hf_configs),
            self.model_weight_path,
        )

    def is_beam_search_kv_cache_sharing_model(self) -> bool:
        return (
            self.model_cls is transformers.GPTJForCausalLM
            and self.optimize_options.kv_cache_sharing_across_beams
        )

    def is_compact_causal_mask_for_bert(self) -> bool:
        return (
            self.model_cls is transformers.BertForQuestionAnswering
            and self.optimize_options.compact_causal_mask
        )

    @staticmethod
    def get_mlperf_options(model_cls: Type[PreTrainedModel]) -> OptimizationConfig:
        if optim_options := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
            return optim_options
        raise NotImplementedError(f"Unsupported mlperf model variant: {model_cls}")

    @staticmethod
    def mlperf_option_exists(model_cls: Type[PreTrainedModel]) -> bool:
        return model_cls in MODEL_CLS_TO_MLPERF_OPT_CONFIGS

    @property
    def contains_mlperf_opts(self) -> bool:
        return ModelMetadata.mlperf_option_exists(  # fmt: off
            self.model_cls
        ) and self.optimize_options.contains(self.get_mlperf_options(self.model_cls))

    def __str__(self):
        # if mlperf_optimized, omit attention type, optimize options because it's fixed
        if self.contains_mlperf_opts:
            maybe_attn_packed_rope = ""
        else:
            # if it's not mlperf nor vanilla attention, add attention type to the model name
            maybe_attn_packed_rope = (
                f"_{self.attention_type.name}"
                if self.attention_type != AttentionType.VANILLA
                else ""
            )
            if self.optimize_options.optimize_packed:
                maybe_attn_packed_rope += "_OPTIMIZED_PACKED"
            if self.optimize_options.optimize_rope:
                maybe_attn_packed_rope += "_ROPE"
            if self.optimize_options.use_rngd_gelu:
                maybe_attn_packed_rope += "_RNGD_GELU"

        name = self.pretrained_id.rsplit("/", maxsplit=1)[-1]

        sliced = self.optimize_options.calculate_logit_only_for_last_token

        return "{}{}{}{}_{}L{}{}{}{}".format(
            "TINY_" if self._is_tiny_gptj else "",
            "FURIOSA_" if self.optimize_options.optimize_furiosa else "",
            name,
            "_LAYERNORM_DECOMPOSED" if self.optimize_options.decompose_layernorm else "",
            self.get_num_hidden_layers(),
            "_MLPERF" if self.contains_mlperf_opts else "",
            "_SLICE" if sliced else "",
            maybe_attn_packed_rope,
            f"_{self.quantization_config}" if self.is_quantized else "",
        )

    @property
    def name(self):
        return self.__str__()

    @property
    def __hash_key(self):
        # The values of self.hf_configs may be a dict or a list, which is not hashable.
        hashable_hf_configs = {
            k: (
                frozenset(v.items())
                if isinstance(v, dict)
                else tuple(v) if isinstance(v, list) else v
            )
            for k, v in self.hf_configs.items()
        }

        return (
            self.pretrained_id,
            self.task_type,
            not self.optimize_options.optimize_furiosa,
            self.hf_configs.get("num_hidden_layers"),
            self.attention_type,
            self.optimize_options,
            self.quantization_config,
            frozenset(hashable_hf_configs.items()),
        )

    def __eq__(self, other):
        if not isinstance(other, ModelMetadata):
            return False
        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, ModelMetadata):
            return NotImplemented
        return self.__hash_key < other.__hash_key

    def __hash__(self):
        return hash(self.__hash_key)

    def get_num_hidden_layers(self) -> int:
        """Retrieve the number of hidden layers in the model.

        If the number of hidden layers was specified during initialization, it returns that value.
        Otherwise, it returns the total number of layers in the model variant.

        Returns:
            int: The number of hidden layers.

        Raises:
            ValueError: If the number of layers in the model variant is unknown.
        """
        return self.hf_configs.get("num_hidden_layers", self.full_layer_count)

    @property
    def pretrained_name(self) -> Optional[str]:
        return self.pretrained_id

    @property
    def is_generative_model(self) -> bool:
        return self.model_cls in transformers.MODEL_FOR_CAUSAL_LM_MAPPING.values()

    @property
    def kv_cache_dtype(self) -> torch.dtype:
        if self.quantization_config:
            if self.quantization_config.kv_cache:
                return self.quantization_config.kv_cache.to_torch_dtype()
            else:
                return torch.float32
        return torch.float32

    @property
    def is_quantized(self) -> bool:
        return self.quantization_config is not None

    @property
    def full_layer_count(self) -> int:
        # FIXME: find better way to get full layer count for LLaMA v3.1 models.
        if self.is_llama3:
            if self.llama_kind == "3.1-8B":
                return 32
            elif self.llama_kind == "3.1-70B":
                return 80
            else:
                raise ValueError(f"Unsupported llama kind: {self.llama_kind}")
        else:
            config = AutoConfig.from_pretrained(self.pretrained_name)

        if full_layer_cnt := getattr(
            config, "num_hidden_layers", getattr(config, "n_layers", None)
        ):
            return full_layer_cnt
        raise ValueError(f"Unknown number of hidden layers for {self}")

    @property
    def config(self) -> PretrainedConfig:
        if self.is_llama3:
            if self.llama_kind == "3.1-8B":
                config = copy.deepcopy(LLAMA3_1_8B_CONFIG)
            elif self.llama_kind == "3.1-70B":
                config = copy.deepcopy(LLAMA3_1_70B_CONFIG)
            else:
                raise ValueError(f"Unsupported llama kind: {self.llama_kind}")

            config.update(self.hf_configs)
            config = transformers.LlamaConfig.from_dict(config)
        else:
            config = AutoConfig.from_pretrained(
                self.pretrained_name,
                **self.hf_configs,
            )

        # This is a workaround to make model with decomposed layernorm distinguishable after instantiation.
        if self.optimize_options.decompose_layernorm:
            config.decompose_layernorm = True

        return config

    @property
    def is_mlperf_optimized(self) -> bool:
        if mlperf_option := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(self.model_cls):
            return self.optimize_options == mlperf_option
        return False

    def is_mlperf_optimized_with(self, **kwargs) -> bool:
        if mlperf_option := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(self.model_cls):
            copied = copy.deepcopy(mlperf_option)
            for k, v in kwargs.items():
                setattr(copied, k, v)
            return self.optimize_options == copied
        return False

    @property
    def llama_kind(self) -> str:
        if self.pretrained_id == LLAMA_7B_PRETRAINED_ID:
            return "1-7B"
        elif self.pretrained_id == LLAMA2_70B_CHAT_PRETRAINED_ID:
            return "2-70B"
        elif self.pretrained_id in (LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID, LLAMA3_1_8B_PRERTRAINED_ID):
            return "3.1-8B"
        elif self.pretrained_id == LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID:
            return "3.1-70B"
        else:
            raise ValueError(f"Unsupported llama model: {self}")

    def get_optimized_cls(self) -> Type[PreTrainedModel]:
        import furiosa_llm_models as flm

        # If no optimization is enabled, return the original model class.
        if not self.optimize_options.get_enabled_opts():
            return self.model_cls

        if self.model_cls is transformers.BertForQuestionAnswering:
            if self.is_mlperf_optimized:
                return flm.bert.symbolic.mlperf_submission.BertForQuestionAnswering
            elif self.optimize_options.compact_causal_mask:
                return (
                    flm.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering
                )
            elif self.optimize_options.optimize_furiosa:
                return flm.bert.symbolic.huggingface.BertForQuestionAnswering
            else:
                raise ValueError(f"Unsupported bert optimized model: {self}")
        elif self.model_cls is transformers.LlamaForCausalLM:
            if self.is_mlperf_optimized:
                if self.is_llama3:
                    return flm.llama3.symbolic.mlperf_submission.LlamaForCausalLM
                else:
                    return flm.llama.symbolic.mlperf_submission.LlamaForCausalLM
            elif self.is_mlperf_optimized_with(calculate_logit_only_for_last_token=True):
                if self.is_llama3:
                    return flm.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM
                else:
                    return flm.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM
            else:
                raise ValueError(f"Unsupported llama model metadata: {self}")
        elif self.model_cls is transformers.GPTJForCausalLM:
            optim_options = self.optimize_options
            assert not optim_options.use_unsplit_packed, "Unsplit packed is not supported for GPT-J"
            if self.is_mlperf_optimized:
                return flm.gptj.symbolic.mlperf_submission.GPTJForCausalLM
            elif self.is_mlperf_optimized_with(calculate_logit_only_for_last_token=True):
                return flm.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM

            # fmt: off
            self_to_cls: Dict[Tuple[AttentionType,FrozenSet[str]],Type[PreTrainedModel]] = {
                (AttentionType.VANILLA, frozenset(("optimize_furiosa",))): flm.gptj.symbolic.huggingface.GPTJForCausalLM,
                (AttentionType.VANILLA, frozenset(("decompose_layernorm",))): transformers.GPTJForCausalLM,
                (AttentionType.VANILLA, frozenset()): transformers.GPTJForCausalLM,
                (AttentionType.VANILLA, frozenset(("optimize_rope",))): flm.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
                (AttentionType.VANILLA, frozenset(("optimize_rope", "use_rngd_gelu"))): flm.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
                (AttentionType.PREALLOCATION_CONCAT, frozenset()): flm.gptj.symbolic.preallocated_concat.GPTJForCausalLM,
                (AttentionType.PREALLOCATION_CONCAT, frozenset(("optimize_rope",))): flm.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
                (AttentionType.PAGED_ATTENTION, frozenset(("optimize_rope",))): flm.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
                (AttentionType.PAGED_ATTENTION, frozenset(("optimize_rope", "optimize_packed", "causal_mask_free_decoding"))): flm.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
            }
            # fmt: on
            assert set(key for keys in self_to_cls.keys() for key in keys[1]).issubset(
                OptimizationConfig().model_dump().keys()
            )

            if cls_ := self_to_cls.get(
                (optim_options.attention_type, self.optimize_options.get_activated_options())
            ):
                return cls_
            else:
                raise ValueError(f"Unsupported model metadata: {repr(self)}")
        return self.model_cls

    @functools.lru_cache(maxsize=1)
    def _random_weight_model(
        self,
        seed: int = TEST_SEED_VALUE,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        # FIXME: This is a workaround to reduce memory usage
        self._pretrained_model.cache_clear()
        if run_gc:
            import gc

            gc.collect()
        set_seed(seed)
        print(f"\x1b[1;36m(Creating {self} with random weights)\x1b[0m", end="", file=sys.stderr)
        sys.stderr.flush()

        ctx_mgr: Union[AbstractContextManager[Any], ContextManager[Any]]
        if self.optimize_options.decompose_layernorm:
            ctx_mgr = replace_layernorm(DecomposedLayerNorm)
        else:
            ctx_mgr = nullcontext()
        with ctx_mgr:
            model = self.get_optimized_cls()(self.config)

        model.eval()
        model.requires_grad_(False)

        if self.optimize_options.decompose_layernorm:
            model.config.decompose_layernorm = True

        if self.is_quantized:
            return self.quantize_model(
                pretrained_model=model, qformat_path=qformat_path, qparam_path=qparam_path
            )
        else:
            return model

    # FIXME: This wraps interal function to properly cache the model(becasue of default args)
    def random_weight_model(
        self,
        seed: int = TEST_SEED_VALUE,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        return self._random_weight_model(seed, qformat_path, qparam_path, run_gc)  # type: ignore[arg-type]

    def load_from_pretrained(self, low_cpu_mem_usage: bool) -> PreTrainedModel:
        if self.is_llama3:
            return self.get_optimized_cls().from_pretrained(
                self.pretrained_name,
                low_cpu_mem_usage=low_cpu_mem_usage,
                config=self.config,
            )
        else:
            return self.get_optimized_cls().from_pretrained(
                self.pretrained_name,
                low_cpu_mem_usage=low_cpu_mem_usage,
                **self.hf_configs,
            )

    @functools.lru_cache(maxsize=PRETRAINED_MODEL_CACHE_SIZE)
    @enforce_torch_load_with_mmap
    def _pretrained_model(
        self,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        prefill_bin_path: Optional[os.PathLike] = None,
        decode_bin_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        # FIXME: This is a workaround to reduce memory usage
        self._random_weight_model.cache_clear()
        if run_gc:
            import gc

            gc.collect()
        print(f"\x1b[1;36m(Loading {self})\x1b[0m", end="", file=sys.stderr)
        sys.stderr.flush()

        low_cpu_mem_usage = True
        load_quantized_state_dict_directly = False

        ctx_mgrs: List[Union[AbstractContextManager[Any], ContextManager[Any]]] = []
        if self.optimize_options.decompose_layernorm:
            ctx_mgrs.append(replace_layernorm(DecomposedLayerNorm))
        if self.is_quantized and (prefill_bin_path or self.state_dict_file_exist()):
            # If state dict file exists, avoid loading original model parameters and do empty weight imitialization.
            import accelerate  # type: ignore[import-untyped]

            # low_cpu_mem_usage should not be enabled when empty weights initialization is used.
            low_cpu_mem_usage = False
            ctx_mgrs.append(accelerate.init_empty_weights())
            logging.info(
                "\x1b[1;35mLoad quantized parameters directly.\x1b[0m",
            )
            load_quantized_state_dict_directly = True

        ctx_mgrs.append(warnings.catch_warnings())

        WARNINGS_TO_IGNORE = [
            ".*copying from a non-meta parameter in the checkpoint to a meta parameter in the current model, which is a no-op..*",
        ]

        # To suppress mcp warning
        class MCPLogFilter(logging.Filter):
            def filter(self, record):
                return (
                    "torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction is enabled. This optimization may affect performance."
                    not in record.msg
                )

        logger = logging.getLogger("create_quantsim_model")
        logger.addFilter(MCPLogFilter())

        with ExitStack() as stack:
            for ctx_mgr in ctx_mgrs:
                stack.enter_context(ctx_mgr)
            warnings.simplefilter(action='ignore', category=FutureWarning)
            for warning_to_ignore in WARNINGS_TO_IGNORE:
                warnings.filterwarnings(action="ignore", message=warning_to_ignore, append=True)

            if load_quantized_state_dict_directly:
                model = self.get_optimized_cls()(self.config)
            else:
                try:
                    with patch("torch.load", new=functools.partial(torch.load, mmap=True)):
                        model = self.load_from_pretrained(low_cpu_mem_usage)
                except OSError:
                    # Error occurs if the model was not saved with `_use_new_zipfile_serialization` option. Try again without mmap option.
                    model = self.load_from_pretrained(low_cpu_mem_usage)

        model.eval()
        model.requires_grad_(False)

        if self.optimize_options.decompose_layernorm:
            model.config.decompose_layernorm = True

        if self.is_quantized:
            return self.quantize_model(
                model,
                qformat_path=qformat_path,
                qparam_path=qparam_path,
                prefill_bin_path=prefill_bin_path,
                decode_bin_path=decode_bin_path,
            )
        else:
            return model

    # FIXME: This wraps interal function to properly cache the model
    def pretrained_model(
        self,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        prefill_bin_path: Optional[os.PathLike] = None,
        decode_bin_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        return self._pretrained_model(qformat_path, qparam_path, prefill_bin_path, decode_bin_path, run_gc)  # type: ignore[arg-type]

    def __get_quant_subpath(self) -> str:
        # FIXME: this is a temporary workaround to get the quantization subpath.
        if self.pretrained_id in TTA_MODEL_PRETRAINED_IDS:
            return "tta_submission"

        if self.is_mlperf_optimized:
            return "mlperf_submission"

        if self.model_cls is transformers.GPTJForCausalLM:
            if self.is_mlperf_optimized_with(calculate_logit_only_for_last_token=True):
                return "mlperf_submission_slice"
            choices = (
                self.attention_type,
                self.optimize_options.optimize_rope,
                self.optimize_options.use_rngd_gelu,
            )
            if choices == (AttentionType.VANILLA, False, False):
                return "original"
            elif choices == (AttentionType.VANILLA, True, False):
                return "preallocated_concat_rope"
            elif choices == (AttentionType.VANILLA, True, True):
                return "huggingface_rope_rngd_gelu"
            elif choices == (AttentionType.PREALLOCATION_CONCAT, True, False):
                return "preallocated_concat_rope"
            elif choices == (AttentionType.PAGED_ATTENTION, True, False):
                if self.optimize_options.optimize_packed:
                    return "paged_attention_optimized_packed_rope"
                else:
                    return "paged_attention_rope"
            else:
                raise ValueError(f"Unsupported model metadata: {self}")
        elif self.model_cls is transformers.BertForQuestionAnswering:
            if self.optimize_options.compact_causal_mask:
                return "compact_causal_mask"
            else:
                raise ValueError(f"Unsupported model metadata: {self}")
        elif self.model_cls is transformers.LlamaForCausalLM:
            if self.is_mlperf_optimized_with(calculate_logit_only_for_last_token=True):
                return "mlperf_submission_slice"
            # We only support optimized packed rope for LLAMA2-70B for now
            assert self.optimize_options.optimize_rope
            assert self.optimize_options.optimize_packed
            assert self.attention_type == AttentionType.PAGED_ATTENTION
            return "paged_attention_optimized_packed_rope"
        else:
            raise ValueError(f"Unsupported model metadata: {self}")

    def state_dict_file_exist(self) -> bool:
        qformat_path, _ = self.qformat_qparam_path()
        return os.path.isfile(Path(qformat_path).parent / "prefill.bin")

    # TODO: add dtype arguments for activation, weight, and kv cache.
    # FIXME: assumes that the furiosa-llm package is located in furiosa-runtime
    def qformat_qparam_path(self) -> Tuple[os.PathLike, os.PathLike]:
        if self._is_tiny_gptj or self.optimize_options.optimize_furiosa:
            root_dir = FURIOSA_LLM_PACKAGE_PATH / "tests" / "quant_files"
        else:
            root_dir = (
                FURIOSA_LLM_PACKAGE_PATH.parent / "furiosa-llm-models-artifacts" / "quantized"
            )
        if not root_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {root_dir}")

        if self.model_cls is transformers.LlamaForCausalLM:
            arch_dir: Optional[str] = "LLaMA" + self.llama_kind
        else:
            arch_dir = MODEL_CLS_TO_QUANT_DIR_NAME.get(self.model_cls)  # type: ignore
        if arch_dir is None:
            raise ValueError(f"Unsupported model variant: {self.model_cls}")
        variant_sub_path = self.__get_quant_subpath()
        tiny_model_suffix = "-tiny" if self._is_tiny_gptj else ""

        # TODO: get filename from quantization target types. (now it's hardcoded to W8A8KV8)
        assert self.quantization_config is not None

        quant_type_path = str(self.quantization_config)

        q_path = (
            root_dir
            / arch_dir
            / variant_sub_path
            / quant_type_path
            / f"{self.get_num_hidden_layers()}L{tiny_model_suffix}"
        )
        # If there's no specific quantization files for specific number of hidden layers,
        # try to use "one for all" quantization files.
        if not os.path.isfile(q_path / "qformat.yaml"):
            full_model_num_layer = self.full_layer_count
            q_path = q_path.parent / f"{full_model_num_layer}L"
            logging.info(
                "\x1b[1;35mFull model qparam/qformat is used for model with smaller number of layers. The model might not be quantized properly.\x1b[0m",
            )
        qformat_path = q_path / "qformat.yaml"
        qparam_path = q_path / "qparam.npy"

        return qformat_path, qparam_path

    def has_side_effect(self) -> bool:
        return self.attention_type == AttentionType.PAGED_ATTENTION

    def quantize_model(
        self,
        pretrained_model: PreTrainedModel,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        prefill_bin_path: Optional[os.PathLike] = None,
        decode_bin_path: Optional[os.PathLike] = None,
    ) -> QuantCausalLM:
        assert self.quantization_config is not None
        if qformat_path is None or qparam_path is None:
            _qformat_path, _qparam_path = self.qformat_qparam_path()

        qformat_path = qformat_path if qformat_path else _qformat_path
        qparam_path = qparam_path if qparam_path else _qparam_path

        if pretrained_model.device == torch.device("meta"):
            prefill_bin_path = prefill_bin_path or Path(qformat_path).parent / "prefill.bin"

            if not os.path.isfile(prefill_bin_path):
                raise ValueError("Prefill bin file for quantization not found")

            if self.is_generative_model:
                decode_bin_path = decode_bin_path or Path(qformat_path).parent / "decode.bin"
                if not os.path.isfile(decode_bin_path):
                    raise ValueError("Decode bin file for quantization not found")
            else:
                if decode_bin_path is not None:
                    raise ValueError(
                        "decode.bin file should not be provided for non-generative model"
                    )
            logger.info(f"Quantize with bin files {prefill_bin_path}, {decode_bin_path}")
        else:
            if prefill_bin_path is not None or decode_bin_path is not None:
                raise ValueError(
                    "Failed to quantize model with bin files. The model should have been created in meta device."
                )

        logging.info(
            f"\x1b[1;35mUsed qparam, qformat path: {qparam_path}, {qformat_path}\x1b[0m",
        )

        return get_quantized_causal_lm(
            pretrained_model,
            qformat_path,
            qparam_path,
            prefill_bin_file_path=prefill_bin_path,
            decode_bin_file_path=decode_bin_path,
        )

    def is_model_available(self) -> bool:
        import furiosa_llm_models

        return not (
            self.is_quantized
            and self.get_optimized_cls()
            in (
                furiosa_llm_models.gptj.symbolic.huggingface.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
                furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
                furiosa_llm_models.llama.symbolic.mlperf_submission.LlamaForCausalLM,
                furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
            )
        )

    def test_uses_models(self) -> Iterable["ModelMetadata"]:
        return [self]

    # FIXME: make this robust
    def is_random_weight_only_model(self) -> bool:
        return "n_embd" in self.hf_configs

    @property
    def is_llama3(self) -> bool:
        return self.pretrained_id in {
            LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID,
            LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID,
            LLAMA3_1_8B_PRERTRAINED_ID,
        }


class Bucket(BaseModel):
    batch_size: int  # batch size, batch size must be a multiple of 2 now.
    attention_size: int

    def input_len(self, is_prefill: bool) -> int:
        if is_prefill:
            return self.attention_size
        else:
            return 1

    def __init__(self, batch_size: int, attention_size: int):
        super(Bucket, self).__init__(batch_size=batch_size, attention_size=attention_size)

    def __hash__(self) -> int:
        return hash((str(self.__class__), self.batch_size, self.attention_size))


# FIXME: CompilerConfigContext must provide more generic way to match between target node and compiler config.
# the following implementation is MLPerf-specific (mostly targets gptj and bert) and should be fixed in the future.
class PagedAttentionConfig(BaseModel):
    """Paged attention configuration.

    Attributes:
        num_blocks (int): The maximum number of blocks that each k/v storage per layer can store
        block_size (int): The maximum number of tokens that can be stored in a single paged attention block
        padding_block_idx (int|None): Padding block's index. This will be used for optimization.
    """

    num_blocks: int
    block_size: int

    # Padding block's index. This will be used for optimization.
    padding_block_idx: Optional[int] = None

    def __init__(self, num_blocks: int, block_size: int, padding_block_idx: Optional[int] = None):
        assert num_blocks > 0
        assert block_size > 0
        super(PagedAttentionConfig, self).__init__(
            num_blocks=num_blocks, block_size=block_size, padding_block_idx=padding_block_idx
        )


class KvCacheSharingAcrossBeamsConfig(BaseModel):
    beam_width: int
    max_new_tokens: int

    def __init__(self, beam_width: int, max_new_tokens: int):
        assert beam_width > 0
        assert max_new_tokens > 0
        super(KvCacheSharingAcrossBeamsConfig, self).__init__(
            beam_width=beam_width, max_new_tokens=max_new_tokens
        )


class ForwardSpec(BaseModel):
    request_type: Literal["prefill", "decode"]
    buckets: List[Bucket]
    paged_attention_config: Optional[PagedAttentionConfig] = None
    # only can be present in decode forward spec
    kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None

    @model_validator(mode="after")
    def check_kv_cache_sharing_across_beams_config(self) -> "ForwardSpec":
        if self.request_type == "prefill":
            assert self.kv_cache_sharing_across_beams_config is None
        return self

    def __init__(
        self,
        request_type: Literal["prefill", "decode"],
        buckets: List[Bucket],
        paged_attention_config: Optional[PagedAttentionConfig] = None,
        kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None,
    ):
        super(ForwardSpec, self).__init__(
            request_type=request_type,
            buckets=buckets,
            paged_attention_config=paged_attention_config,
            kv_cache_sharing_across_beams_config=kv_cache_sharing_across_beams_config,
        )


# # TODO: Use this LLMTC (working title) to refactor test suites
# class LLMTC(BaseModel):
#     # This model_config is FOR pydantic to allow mppp field
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     model_metadata: ModelMetadata
#     forward_specs: List[ForwardSpec]
#     mppp: Mppp

#     @model_validator(mode="after")
#     def check_paged_attention_config(self) -> "LLMTC":
#         if self.model_metadata.attention_type == AttentionType.PAGED_ATTENTION:
#             for forward_spec in self.forward_specs:
#                 assert forward_spec.paged_attention_config is not None
#         return self
