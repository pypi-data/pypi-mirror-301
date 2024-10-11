from dataclasses import dataclass
import glob
import logging
import os
from pathlib import Path
from typing import Mapping, Optional

import yaml

from furiosa_llm.models import Bucket
from furiosa_llm.parallelize.pipeline.types import BlockType, PipelineMode


# FIXME: CompilerConfigContext must provide more generic way to match between target node and compiler config.
# the following implementation is MLPerf-specific (mostly targets gptj and bert) and should be fixed in the future.
@dataclass
class CompilerConfigContext:
    # Fully quanlified model class name, e.g. "furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM"
    model_qname: str

    num_pe: Optional[int] = None
    block_type: Optional[BlockType] = None
    bucket: Optional[Bucket] = None
    phase: Optional[PipelineMode] = None
    beam_size: Optional[int] = None
    compiler_config_overrides: Optional[Mapping] = None

    @property
    def location(self) -> Optional[Path]:
        minimized_model_type = self.model_qname
        if "gptj" in self.model_qname.lower():
            minimized_model_type = "gptj"
        elif "bert" in self.model_qname.lower():
            minimized_model_type = "bert"
        elif "llama" in self.model_qname.lower():
            minimized_model_type = "llama"
        else:
            return None

        if self.num_pe is None or self.block_type is None or self.bucket is None:
            return None

        if (
            self.phase is None
            or self.phase == PipelineMode.UNKNOWN
            # FIXME: MLPerf specific implementation
            # bert does not have phase, but furiosa-llm handle it as "prefill" as a workaround, while compiler does not.
            or minimized_model_type == "bert"
        ):
            phase_block = self.block_type.value
        else:
            phase_block = f"{self.phase.value}_{self.block_type.value}"

        # FIXME: the batch size we call is different between compiler team and platform team.
        # the config file name is generated based on the compiler team's definition, which is `/ beam_size` of the platform team's definition.
        # this might be mlperf-specific and should be fixed in the future.
        if self.phase == PipelineMode.LLM_DECODE and self.beam_size is not None:
            b = self.bucket.batch_size // self.beam_size
        else:
            b = self.bucket.batch_size
        s = self.bucket.attention_size
        return Path(
            f"/usr/share/furiosa/compiler/configs/{minimized_model_type}_{self.num_pe}pe_{phase_block}_b{b}_s{s}.yaml"
        )

    # The fallback location to look for compiler config.
    # The rule is decided heuristically, and current rule is: look for matching (model, num_pe, phase, block), and tolerate bucket mismatches.
    def fallback_location(self) -> Optional[Path]:
        if self.block_type is None or self.num_pe is None:
            return None
        if any(s in self.model_qname.lower() for s in ("gptj", "gpt_j", "gpt-j")):
            if self.phase == PipelineMode.LLM_PREFILL:
                pat = f"gptj_{self.num_pe}pe_prefill_{self.block_type.value}*.yaml"
            else:
                pat = f"gptj_{self.num_pe}pe_decode_{self.block_type.value}*.yaml"
        elif "bert" in self.model_qname.lower():
            pat = f"bert_{self.num_pe}pe_{self.block_type.value}*.yaml"
        elif "llama" in self.model_qname.lower():
            if self.phase == PipelineMode.LLM_PREFILL:
                pat = f"llama*_{self.num_pe}pe_prefill_{self.block_type.value}*.yaml"
            else:
                pat = f"llama*_{self.num_pe}pe_decode_{self.block_type.value}*.yaml"
        else:
            return None
        matches = glob.glob(f"/usr/share/furiosa/compiler/configs/{pat}")
        if matches:
            return Path(matches[0])
        return None

    def default_config(self) -> Mapping:
        if self.phase == PipelineMode.LLM_PREFILL:
            tactic_hint = "ForLlmModelPrefill"
        elif self.phase == PipelineMode.LLM_DECODE:
            tactic_hint = "ForLlmModelDecode"
        else:
            tactic_hint = "Default"  # XXX: for non-generative models

        return {
            "populator_mode": "General",
            "allow_unlowered_operators": False,
            "implicit_type_casting": False,
            "lowering_mode": "Optimal",
            "tactic_hint": tactic_hint,
        }

    def load_config(self) -> Mapping:
        config: Optional[Mapping] = None
        if self.location and os.path.exists(self.location):
            logging.info(f"Using compiler config from {self.location}")
            config = yaml.safe_load(open(self.location))
        elif (fallback := self.fallback_location()) and os.path.exists(fallback):
            logging.info(f"Failed to locate compiler config from {self.location}")
            logging.info(f"Using fallback compiler config from {fallback}")
            config = yaml.safe_load(open(fallback))
        if config is None:
            logging.info(
                f"Failed to locate compiler config from {self.location} and fallback location (context={self})"
            )
            logging.info("Using default compiler config")
            config = self.default_config()
        if self.can_use_tactic_hint():
            config = {**config, **self.get_tactic_hint()}
        if self.compiler_config_overrides is not None:
            config = {**config, **self.compiler_config_overrides}
        return config

    def can_use_tactic_hint(self) -> bool:
        if not os.environ.get("ENABLE_SELECTED_TACTIC_HINT", "0") == "1":
            return False
        if self.location is None:
            return False
        if not os.path.exists(self.location):
            return False
        if "gptj" in self.model_qname.lower() and "slice" not in self.model_qname.lower():
            return False
        return True

    def get_tactic_hint(self) -> Mapping:
        assert self.can_use_tactic_hint()
        assert self.location is not None
        return {"SelectedTactics": self.location.with_suffix("").absolute().as_posix()}
