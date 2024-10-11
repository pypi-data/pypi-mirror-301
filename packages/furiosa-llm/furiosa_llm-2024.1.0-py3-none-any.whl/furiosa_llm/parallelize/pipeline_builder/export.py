import os
from typing import Dict, Mapping, Union

from safetensors import safe_open
from safetensors.torch import _find_shared_tensors, save_file
import torch

from furiosa_llm.parallelize.pipeline.types import ParamfileFormat


def _tensors_with_same_storage_and_length(tensor1: torch.Tensor, tensor2: torch.Tensor) -> bool:
    return (
        tensor1.data_ptr() == tensor2.data_ptr()
        and tensor1.nelement() == tensor2.nelement()
        and tensor1.dtype == tensor2.dtype
    )


def save_tensors(
    tensors: Mapping[str, torch.Tensor],
    path: Union[str, os.PathLike],
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
):
    if format == ParamfileFormat.SAFETENSORS:
        tensors_ = dict(tensors)

        # This is needed because `_find_shared_tensors` calls `view(-1)` to get tensor's address range.
        # TODO: find way to check overlapping tensors without making it contiguous.
        for name, tensor in tensors_.items():
            try:
                tensor.view(-1)
            except RuntimeError:
                tensors_[name] = tensor.contiguous()

        shared_pointers = _find_shared_tensors(tensors_)

        # This is a workaround for shared tensors in model dict. (`Link shared tensor <https://huggingface.co/docs/safetensors/en/torch_shared_tensors>`_).
        # ``save_model`` API can save shared tensors, but individual shared tensor cannot be loaded from it because only one of shared tensors
        # covering the entire buffer are stored. Even if there is a mapping between excluded tensors to stored one, this is not
        # sufficient because it doesn't include which part of the stored one is excluded one. So, we now restrict all shared tensors to have
        # exactly same data ptr and length, and this can cover most of the cases we are interested in.
        metadata = {}

        for names in shared_pointers:
            if len(names) > 1:
                names_ = list(names)
                # To enforce same representative tensor across executions.
                names_.sort()
                for name in names_[1:]:
                    # TODO: find a way to handle shared tensors that are not exactly same.
                    if not _tensors_with_same_storage_and_length(tensors[name], tensors[names_[0]]):
                        raise RuntimeError(
                            "Shared tensors that are not exactly same cannot be saved right now"
                        )
                    # save mapping info for excluded one to stored one.
                    metadata[name] = names_[0]
                    del tensors_[name]

        # Make all tensors contigous before saving.
        tensors_ = {k: v.contiguous() for k, v in tensors_.items()}

        save_file(tensors_, path, metadata)
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


def load_tensors(
    path: os.PathLike, format: ParamfileFormat = ParamfileFormat.SAFETENSORS
) -> Mapping[str, torch.Tensor]:
    tensors: Dict[str, torch.Tensor] = {}

    if format == ParamfileFormat.SAFETENSORS:
        # The example shows safe_open with 'with clause'; https://huggingface.co/docs/safetensors/index
        # It still causes 'error: "safe_open" has no attribute "__enter__"'. Why? for workaround, ignore it.
        with safe_open(path, framework="pt", device="cpu") as f:  # type: ignore
            for key in f.keys():
                tensors[key] = f.get_tensor(key)
        return tensors
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")
