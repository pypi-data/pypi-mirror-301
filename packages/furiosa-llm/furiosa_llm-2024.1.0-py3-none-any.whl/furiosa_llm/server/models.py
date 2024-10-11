from argparse import Namespace
import logging
import os
import re
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
import uuid

from transformers import AutoTokenizer

from furiosa_llm.api import LLM
from furiosa_llm.outputs import CompletionOutput, RequestOutput
from furiosa_llm.sampling_params import SamplingParams
from furiosa_llm.server.parse import parse_and_batch_prompt  # type: ignore
from furiosa_llm.tokenizer import encode_auto

logger = logging.getLogger(__name__)


def load_llm_from_args(args: Namespace) -> LLM:
    model: str = args.model
    dp = args.data_parallel_size
    devices = args.devices

    # if model is a directory and "ready" file exists, it is an artifact
    use_artifact_from_path = os.path.isdir(model) and os.path.exists(os.path.join(model, "ready"))

    if use_artifact_from_path:
        logger.info(f"Loading LLM from artifact: {model}")
        if any([args.tensor_parallel_size, args.pipeline_parallel_size]):
            logger.warning(
                "When loading LLM from artifact, given -tp and -pp values will be ignored."
            )
        return LLM.from_artifacts(
            model,
            data_parallel_size=dp,
            devices=devices,
        )

    if model == "furiosa-ai/fake-llm":
        return FakeLLM()

    # XXX: for Furiosa SDK 2024.1 (alpha), we do not support direct compilation of Hugging Face models.
    # TODO: remove this block when we support direct compilation of Hugging Face models.
    raise FileNotFoundError(
        "for Furiosa SDK 2024.1 (alpha), only loading from artifact is supported.\n"
        f"given artifact path is invalid: {model}"
    )

    if not is_hf_model_id_like(model):
        logger.warning(
            f"The given --model argument is not a valid artifact path, nor a valid Hugging Face model id: {model}"
        )
        logger.warning("Trying Hugging Face model id anyways.")

    tp = args.tensor_parallel_size or 4
    pp = args.pipeline_parallel_size or 1
    logger.info(
        f"Loading LLM from Hugging Face model id: {model}, pp={pp}, tp={tp}, dp={dp}, devices={devices}"
    )
    return LLM(
        model,
        pipeline_parallel_size=pp,
        tensor_parallel_size=tp,
        data_parallel_size=dp,
        devices=devices,
    )


def is_hf_model_id_like(model_id: str) -> bool:
    pattern = r"^[\w-]+/[\w.-]+$"
    return bool(re.match(pattern, model_id))


class FakeLLM(LLM):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        self.text_output = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.token_output = self.tokenizer.encode(self.text_output)
        self.is_generative_model = True

    @property
    def model_max_seq_len(self) -> int:
        return 2048

    def generate(
        self,
        prompts: Union[str | List[str]],
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[Union[List[int], List[List[int]]]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
    ) -> RequestOutput | List[RequestOutput]:
        parsed_prompts = parse_and_batch_prompt(prompts or prompt_token_ids)
        num_prompts = len(parsed_prompts)
        prompt_strs = []
        for prompt in parsed_prompts:
            if prompt['is_tokens']:
                prompt_strs.append(
                    self.tokenizer.decode(prompt['content'], skip_special_tokens=True)
                )
            else:
                prompt_strs.append(prompt['content'])

        if num_prompts == 1:
            return self.lorem_ipsum_output(prompt_strs[0], sampling_params)
        else:
            return [self.lorem_ipsum_output(prompt, sampling_params) for prompt in prompt_strs]

    async def stream_generate(
        self,
        prompt: str,
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        is_demo: bool = False,
    ) -> AsyncGenerator[str, None]:
        assert prompt_token_ids is None
        for token in self.token_output[: sampling_params.max_tokens]:
            yield self.tokenizer.decode([token], skip_special_tokens=True)

    def lorem_ipsum_output(
        self, prompt: str, sampling_params: SamplingParams, finish_reason: Optional[str] = "stop"
    ) -> RequestOutput:
        token_output = self.token_output[: sampling_params.max_tokens]
        return RequestOutput(
            # request_id will be overwritten by handlers
            request_id=uuid.uuid4().hex,
            prompt=prompt,
            prompt_token_ids=encode_auto(self.tokenizer, prompt)['input_ids'],
            outputs=[
                CompletionOutput(
                    index=0,
                    text=self.tokenizer.decode(token_output, skip_special_tokens=True),
                    token_ids=token_output,
                    finish_reason=finish_reason,
                )
            ],
            finished=True,
        )
