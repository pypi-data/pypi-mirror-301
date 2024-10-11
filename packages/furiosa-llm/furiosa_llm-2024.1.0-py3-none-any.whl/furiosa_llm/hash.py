import dataclasses
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence, Tuple, Type

import torch
from torch.utils._pytree import tree_map_only
import transformers
from transformers import PretrainedConfig

FURIOSA_RT_DIR = Path(__file__).parent.parent.parent
FURIOSA_LLM_MODELS_DIR = FURIOSA_RT_DIR / "furiosa-llm-models"
FURIOSA_LLM_MODELS_ARTIFACTS_DIR = FURIOSA_RT_DIR / "furiosa-llm-models-artifacts"
MODEL_COMPRESSOR_DIR = FURIOSA_RT_DIR / "furiosa-llm-models-artifacts"


def get_env_independent_hash(val: Any) -> str:
    hasher = hashlib.sha256()
    if isinstance(val, (list, tuple)):
        for elem in val:
            hasher.update(get_env_independent_hash(elem).encode())
    else:
        if dataclasses.is_dataclass(val):
            val = json.dumps(dataclasses.asdict(val), sort_keys=True, indent=2)  # type: ignore[call-overload]
        hasher.update(str(val).encode())
    return hasher.hexdigest()


def hash_model(
    original_model_type: Type,
    model_config: PretrainedConfig,
    qformat_qparam_path: Optional[Tuple[os.PathLike, os.PathLike]],
    pretrained_id: str,
    seed: Optional[int],
    is_random_weight_model: bool,
    extra_args: Mapping[str, str] = {},
) -> str:
    import git

    if is_random_weight_model and seed is None:
        raise ValueError(
            "When `is_random_weight_model` is True, `seed` should not be None to determine weight value is same."
        )

    weight_hash = str(seed) if is_random_weight_model else pretrained_id

    to_be_hashed = [
        str(original_model_type),
        model_config.to_json_string(),
        weight_hash,
    ]

    # Add version info of the model
    if original_model_type.__module__.startswith("furiosa_llm_models"):
        to_be_hashed.append(git.Repo(FURIOSA_LLM_MODELS_DIR).head.object.hexsha)
    elif original_model_type.__module__.startswith("transformers"):
        to_be_hashed.append(transformers.__version__)
    else:
        raise NotImplementedError(f"unhashable model class module: {original_model_type}")

    # Add quantization info if quantized
    if qformat_qparam_path is not None:
        mcp_version = git.Repo(MODEL_COMPRESSOR_DIR).head.object.hexsha
        qfile_commit_ids = (
            git.Repo(path, search_parent_directories=True).head.object.hexsha
            for path in qformat_qparam_path
        )
        qfile_paths = (os.fspath(path) for path in qformat_qparam_path)

        to_be_hashed.append(mcp_version)
        to_be_hashed.extend(qfile_paths)
        to_be_hashed.extend(qfile_commit_ids)

    if extra_args:
        to_be_hashed.append(json.dumps(extra_args, sort_keys=True))

    return get_env_independent_hash(to_be_hashed)


def hash_example_inputs(
    example_args: Sequence,
    example_kwargs: Mapping,
) -> str:
    return get_env_independent_hash(
        json.dumps(
            tree_map_only(
                torch.Tensor,
                lambda t: (t.shape, str(t.dtype), t.stride(), str(t.device)),
                (example_args, example_kwargs),
            ),
            sort_keys=True,
            indent=2,
        ),
    )
