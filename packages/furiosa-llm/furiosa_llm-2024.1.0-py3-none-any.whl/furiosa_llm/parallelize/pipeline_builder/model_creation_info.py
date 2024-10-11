from dataclasses import dataclass
import os
import typing
from typing import Optional, Tuple

from transformers import PreTrainedModel

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata


@dataclass(frozen=True)
class ModelCreationInfo:
    metadata: "ModelMetadata"
    random_weight_model: bool
    seed: Optional[int] = None
    qformat_path: Optional[os.PathLike] = None
    qparam_path: Optional[os.PathLike] = None
    prefill_quant_bin_path: Optional[os.PathLike] = None
    decode_quant_bin_path: Optional[os.PathLike] = None

    def instantiate_model(self) -> PreTrainedModel:
        if self.random_weight_model:
            return self.metadata.random_weight_model(
                qformat_path=self.qformat_path, qparam_path=self.qparam_path
            )
        else:
            return self.metadata.pretrained_model(
                qformat_path=self.qformat_path,
                qparam_path=self.qparam_path,
                prefill_bin_path=self.prefill_quant_bin_path,
                decode_bin_path=self.decode_quant_bin_path,
            )

    def get_qparam_qformat_path(self) -> Optional[Tuple[os.PathLike, os.PathLike]]:
        if not self.metadata.is_quantized:
            return None
        default_qformat_qparam_path = self.metadata.qformat_qparam_path()
        return (
            self.qformat_path if self.qformat_path else default_qformat_qparam_path[0],
            self.qparam_path if self.qparam_path else default_qformat_qparam_path[1],
        )

    def is_hashable(self) -> bool:
        return not self.random_weight_model or self.seed is not None
