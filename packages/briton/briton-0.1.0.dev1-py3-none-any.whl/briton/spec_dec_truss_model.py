import os
import random



DEVELOPMENT_MODE = os.environ.get("TRUSS_DEVELOPMENT_MODE", "false").lower() == "true"


from itertools import count
from pathlib import Path
from typing import List, Optional, cast
import asyncio
import logging
import os
import time

import briton.briton_pb2
import briton.briton_pb2_grpc

import fastapi
from fastapi import HTTPException as FastApiHTTPException
from briton.fsm_cache import FsmCache
from briton.schema import ModelInput
from transformers import AutoTokenizer, PreTrainedTokenizerFast
from briton.flags import TRUSS_DEVELOPMENT_MODE
from briton.fs import is_local_path
from briton.briton import BritonInteractor, BritonInteractorImpl
from briton.spec_dec import handle_request_exception, worker, SpecDecRequest, pick_tokens_from_end
from briton.error_handling import grpc_error_handling
from briton.data_structures import common_prefix_length
from briton.errors import HTTPException as BritonHTTPException

# TODO(pankaj) Pick this from truss constants, once a small lib is extracted out of truss.
OPENAI_COMPATIBLE_TAG = "openai-compatible"

TARGET_PORT = 50051
DRAFT_PORT = 50052
DEFAULT_TP_COUNT = 1

# Relative to data dir
TARGET_MODEL_PATH = "target"
DRAFT_MODEL_PATH = "draft"

# Use a directory that can be picked up by baseten-fs, if enabled
FSM_CACHE_DIR = "/cache/model/fsm_cache"

logger = logging.getLogger(__name__)


MODEL_INPUT_TO_BRITON_FIELD = {
    "max_tokens": "request_output_len",
    "beam_width": "beam_width",
    "repetition_penalty": "repetition_penalty",
    "presence_penalty": "presence_penalty",
    "temperature": "temperature",
    "length_penalty": "len_penalty",
    "end_id": "end_id",
    "pad_id": "pad_id",
    "runtime_top_k": "runtime_top_k",
    "runtime_top_p": "runtime_top_p",
    "random_seed": "random_seed",
}


class Model:
    def __init__(self, **kwargs):
        self._loaded = False
        self._model = None
        self._config = kwargs["config"]
        self._data_dir = kwargs["data_dir"]
        self._secrets = kwargs["secrets"]
        self._request_id_counter = count(start=1)
        model_metadata = self._config.get("model_metadata", {})
        _openai_compatiblilty_check(model_metadata)

        self._tp_count = model_metadata.get("tp_count", DEFAULT_TP_COUNT)
        self._hf_tokenizer = _get_model_metadata_or_raise(model_metadata, "hf_tokenizer")
        self._tool_call_token_id = _get_model_metadata_or_raise(
            model_metadata, "tool_call_token_id"
        )
        if not TRUSS_DEVELOPMENT_MODE:
          self._hf_spec_dec_repo_id = _get_model_metadata_or_raise(model_metadata, "hf_spec_dec_repo_id")

        self._target_kv_cache_free_gpu_mem_fraction = \
            _get_model_metadata_or_raise(model_metadata, "target_kv_cache_free_gpu_mem_fraction")
        self._draft_kv_cache_free_gpu_mem_fraction = \
            _get_model_metadata_or_raise(model_metadata, "draft_kv_cache_free_gpu_mem_fraction")
        self._num_draft_max_input_tokens = \
            _get_model_metadata_or_raise(model_metadata, "num_draft_max_input_tokens")
        self._draft_max_num_tokens = model_metadata.get("draft_max_num_tokens", None)
        self._target_max_num_tokens = model_metadata.get("target_max_num_tokens", None)
        self._enable_chunked_context = model_metadata.get("enable_chunked_context", False)
        self._total_token_limit = model_metadata.get("total_token_limit", None)
        self._num_draft_tokens = _get_model_metadata_or_raise(model_metadata, "num_draft_tokens")
        self._hf_token = _get_hf_token_or_none(self._secrets)
        self._lazy_init_done = False
        self._lazy_init_lock = None
        self._draft_stub = None
        self._target_stub = None
        self._draft_queue = None
        self._target_queue = None
        self._max_fsm_workers = 10

        # Total tokens input tokens in flight. 
        # TODO(pankaj) Take generated tokens into account as well. That has to
        # be done carefully to avoid any performance impact. Going with this
        # simple mechanism for now.
        self._total_tokens_lock = None
        self._total_tokens = 0

        # Allow passing briton_interactor for ease of testing
        self._briton_interactor: BritonInteractor = \
          model_metadata.get("briton_interactor", BritonInteractorImpl())

    def load(self):
        if self._loaded:
            return

        # todo: Use special briton interactor for development mode
        self._briton_interactor.hf_download(self._hf_spec_dec_repo_id, local_dir=self._data_dir, hf_token=self._hf_token)

        if is_local_path(self._data_dir / self._hf_tokenizer):
          self._tokenizer = AutoTokenizer.from_pretrained(self._data_dir / self._hf_tokenizer)
        else:
          self._tokenizer = AutoTokenizer.from_pretrained(self._hf_tokenizer)

        # We only support Llama and mistral with Briton, for which this should
        # apply.
        assert isinstance(self._tokenizer, PreTrainedTokenizerFast)

        # These are tokens outside of tokenizer.json. We need to pass these to
        # Briton, to pass to rust tokenizer.
        added_token_decoders = self._tokenizer.added_tokens_decoder
        added_tokens = [token for token in added_token_decoders.values()]

        # We want rust tokenizer to load from file. If hf_tokenizer is a remote
        # repo then we download it locally.
        if is_local_path(self._data_dir / self._hf_tokenizer):
            self._saved_tokenizer_dir = self._data_dir / self._hf_tokenizer
        else:
            # data_dir should have a target and draft subdirectory. Creating this
            # directory shouldn't have a name conflict with those.
            self._saved_tokenizer_dir = str(self._data_dir / "saved_tokenizer")
            self._tokenizer.save_pretrained(self._saved_tokenizer_dir)

        # Initialize n processes for _max_fsm_workers
        self._fsm_cache = FsmCache(
            Path(FSM_CACHE_DIR), self._tokenizer, self._max_fsm_workers, self._tool_call_token_id
        )

        load_briton = self._briton_interactor.load
        load_briton(
            model_name="target",
            engine_path=(self._data_dir / TARGET_MODEL_PATH),
            hf_tokenizer=self._saved_tokenizer_dir,
            work_dir=(self._data_dir / "target"),
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._target_kv_cache_free_gpu_mem_fraction,
            port=TARGET_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._target_max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
        )
        load_briton(
            model_name="draft",
            engine_path=(self._data_dir / DRAFT_MODEL_PATH),
            hf_tokenizer=self._saved_tokenizer_dir,
            work_dir=(self._data_dir / "draft"),
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._target_kv_cache_free_gpu_mem_fraction,
            port=DRAFT_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._draft_max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
        )
        self._loaded = True

    async def predict(self, model_input, request: fastapi.Request):
        """
        Run inference

        Note that the async nature of this function is a little tricky. Care is
        needed to make sure this function is a regular async function and not an
        async generator, i.e. there shouldn't be any direct yields in this
        function. This is because we need to support both streaming and
        non-streaming cases in this function. We do this by either returning an
        async-generator for the streaming case, or directly the full text for
        the other case. Returning an async generator for non-streaming case
        interferes with the open ai client proxy.
        """
        async def is_cancelled_fn():
            disconnected = await request.is_disconnected()
            if disconnected:
                logger.info("Request disconnected, cancelling.")
            return disconnected

        if not self._lazy_init_done:
            # While this isn't completely safe, the async lock needs to be
            # created within the same async loop where it will be used. Ideally,
            # the proper solution would involve supporting asynchronous load
            # function, but that is not currently supported in Truss. The risk is
            # that multiple initial requests could end up with different lock
            # instances, making the lock ineffective. In practice, this is
            # highly unlikely. This issue could occur if one request executes
            # the line below and then gets preempted, allowing another request
            # to execute the same line. However, since there is no async
            # operation in the following line, it is very unlikely for the
            # request to be preempted at that point.
            if self._lazy_init_lock is None:
                self._lazy_init_lock = asyncio.Lock()

            async with self._lazy_init_lock:
                self._total_tokens_lock = asyncio.Lock()
                self._target_stub = self._briton_interactor.create_grpc_stub(TARGET_PORT)
                self._draft_stub = self._briton_interactor.create_grpc_stub(DRAFT_PORT)
                self._target_queue = asyncio.Queue()
                self._draft_queue = asyncio.Queue()
                asyncio.create_task(worker(
                    self._target_queue,
                    self._target_consumer,
                    self._draft_queue,
                    self._draft_consumer,
                    asyncio.Event(),
                ))
                self._lazy_init_done = True

        val_model_input = ModelInput(**model_input)
        prompt = val_model_input.prompt(cast(PreTrainedTokenizerFast, self._tokenizer))
        model_input.pop("messages", None)
        input_ids = self._tokenizer(prompt).input_ids

        schema_hash = None
        schema = val_model_input.output_json_schema
        if schema is not None:
            schema_hash = await self._fsm_cache.add_schema(schema)

        req = SpecDecRequest(
            id=self._calc_request_id(),
            input_ids=input_ids,
            draft_ids=[],
            model_input=model_input,
            is_cancelled_fn=is_cancelled_fn,
            output_schema_hash=schema_hash,
            force_tools=val_model_input.force_tools,
        )

        # Wait for space in the total token limit.
        while self._total_tokens + len(input_ids) > self._total_token_limit:
            if await req.is_cancelled_fn():
                raise RuntimeError("Request cancelled")
            await asyncio.sleep(0.01)

        # Reserver space in total tokens before queueing
        async with self._total_tokens_lock:
            self._total_tokens += len(req.input_ids)
        self._target_queue.put_nowait(req)

        async def read_req_queue():
            while True:
                inc_text = await req.queue.get()
                if inc_text is None:
                    break
                if isinstance(inc_text, BritonHTTPException):
                    raise FastApiHTTPException(
                      status_code=inc_text.status_code, 
                      detail=inc_text.detail,
                    )
                yield inc_text

            # When done, release space from total tokens.
            async with self._total_tokens_lock:
                self._total_tokens -= len(req.input_ids)

        logger.debug(f"Input ids: {input_ids}")
        # spec_dec_async_gen = await read_req_queue()
        if model_input.get("stream", True):
            return read_req_queue()
        else:
            return await _collect_text(read_req_queue)

    def _calc_request_id(self) -> int:
        """Calculate unique request id.

        Not thread safe, but safe to use in single threaded async context. There
        are no async operations here, so this function is unlikely to be
        preempted in the middle. This is important otherwise we may end up with
        duplicate ids.
        """
        return int(str(os.getpid()) + str(next(self._request_id_counter)))

    async def _call_draft(self, request_id: int, req: SpecDecRequest, batch_request_ids: List[int]):
        """Call draft model.

        This request is part of a batch of requests. All batch requests ids need to be
        provided in batch_request_ids.
        """
        # Draft model may only support a smaller context, so limit input tokens
        # to it.
        draft_tokens_start = \
            pick_tokens_from_end(len(req.input_ids), self._num_draft_max_input_tokens)
        request = briton.briton_pb2.InferenceRequest(
            request_id=request_id,
            input_ids=req.input_ids[draft_tokens_start:],
            request_output_len=self._num_draft_tokens,
            batch=briton.briton_pb2.Batch(
                request_ids=batch_request_ids
            ),
            output_schema_hash=req.output_schema_hash,
            fsm_state=req.fsm_state,
            force_tools=req.force_tools,
        )
        self._update_request_end_id_pad_id(request, req.model_input)
        with grpc_error_handling():
            resp_iter = self._draft_stub.Infer(request)
            draft_output_ids = []
            async for delta in resp_iter:
                draft_output_ids.extend(delta.output_ids)
        return draft_output_ids

    async def _call_target(
        self, 
        request_id: int, 
        req: SpecDecRequest,
        batch_request_ids: List[int],
        max_tokens: Optional[int],
    ):
        """Call target model.

        This request is part of a batch of requests. All batch requests ids need to be
        provided in batch_request_ids.
        Proposed draft ids should be provided in draft_ids.
        Target model request needs all the sampling params.

        max_tokens is the maximum number of tokens to generate. Note that target model
        can generate more than one token due to draft token acceptance. max_tokens can
        be used to cut this short to adhere to the max tokens limit at request level.
        """
        request_output_len = self._num_draft_tokens + 1
        if max_tokens is not None:
            request_output_len = min(request_output_len, max_tokens)

        request = briton.briton_pb2.InferenceRequest(
            request_id=request_id,
            input_ids=req.input_ids,
            draft_input_ids=req.draft_ids,
            request_output_len=request_output_len,
            batch=briton.briton_pb2.Batch(
                request_ids=batch_request_ids
            ),
            fsm_state=req.fsm_state,
            force_tools=req.force_tools,
            write_output_states=True,  # The target should always write its state
        )
        self._update_request_end_id_pad_id(request, req.model_input)
        set_briton_request_fields_from_model_input(req.model_input, request)
        for words in ["bad_words", "stop_words"]:
            if words in req.model_input:
                for word in req.model_input[words].split(","):
                    getattr(request, words).append(word)
        with grpc_error_handling():
            resp_iter = self._target_stub.Infer(request)
            target_text = ""
            target_output_ids = []
            target_output_states = []

            eos_encountered = False
            max_tokens_reached = False
            async for delta in resp_iter:
                # TODO(pankaj): decide on whether to return eos token.
                # Do not include for now.
                if self._eos_token_id() in delta.output_ids:
                    eos_token_id_index = list(delta.output_ids).index(self._eos_token_id())
                    target_output_ids.extend(delta.output_ids[:eos_token_id_index])
                    eos_index = delta.output_text.find(self._eos_token())
                    if eos_index != -1:
                        target_text += delta.output_text[:eos_index]
                    eos_encountered = True
                    break

                target_output_ids.extend(delta.output_ids)
                target_output_states.extend(delta.output_states)

                # Note that output_text may be empty string and that's ok.
                # Briton may be buffering for unicode characters.
                target_text += delta.output_text

                # TODO(pankaj): Cut exactly at max_tokens. We let the tokens go
                # a little bit over right now as mapping subset of tokens to
                # text is a little tricky. 
                # Also ideally batch manager should honor the request_output_len above
                # but it doesn't seem to in this draft acceptance case.
                if max_tokens is not None and len(target_output_ids) >= max_tokens:
                    max_tokens_reached = True
                    break

        return (
            target_output_ids, 
            target_output_states,
            target_text, 
            eos_encountered, 
            max_tokens_reached,
        )

    def _eos_token(self):
        return getattr(self._tokenizer, "eos_token", None)

    def _eos_token_id(self):
        return getattr(self._tokenizer, "eos_token_id", None)

    def _pad_token_id(self):
        return getattr(self._tokenizer, "pad_token_id", None)

    def _update_request_end_id_pad_id(self, request, model_input):
        end_id = model_input.get("end_id", None) or self._eos_token_id()
        if end_id is not None:
            request.end_id = end_id
        pad_id = model_input.get("pad_id", None) or self._pad_token_id() 
        if pad_id is not None:
            request.pad_id = pad_id

    def _set_default_random_seed(self, request):
        request.random_seed = random.randint(-(2**63), 2**63 - 1)

    async def _target_consumer(self, requests: List[SpecDecRequest]) -> List[SpecDecRequest]:
        """Consumes requests from the target queue and fetches predictions from target model.

        Args:
            requests (List[Request]): Requests to process

        Returns:
            List[Request]: Requests to continue.
        """
        @handle_request_exception
        async def call_target(req, req_id, batch_request_ids):
            max_tokens = req.model_input.get("max_tokens", None)
            max_incremental_target_tokens = max_tokens - req.produced_token_count if max_tokens is not None else None
            st = time.time()
            (
                target_output_ids,
                target_output_states,
                target_text,
                eos_encountered,
                max_tokens_reached,
            ) = await self._call_target(
                req_id,
                req,
                batch_request_ids,
                max_incremental_target_tokens,
            )
            req.target_time_ms += (time.time() - st) * 1000
            # Streaming return target_text
            req.queue.put_nowait(target_text)
            req.produced_token_count += len(target_output_ids)
            req.iterations += 1
            accepted_count = common_prefix_length(req.draft_ids, target_output_ids)
            req.accepted_token_count += accepted_count
            
            def should_stop():
                if eos_encountered:
                    logger.debug("eos encountered")
                    return True

                if max_tokens_reached:
                    logger.debug("Reached max tokens, stopping")
                    return True

                if len(target_output_ids) == 0:
                    logger.debug("Target output is empty, stopping")
                    return True

                if target_output_ids == req.draft_ids:
                    logger.debug("Draft and target outputs are the same, stopping")
                    return True
                return False
            
            # Stopping conditions and cancellation handling.
            if should_stop() or await req.is_cancelled_fn():
                logger.info(f"Total generated token count: {req.produced_token_count}")
                logger.info(f"Total draft token count: {req.draft_token_count}")
                logger.info(f"Total draft time: {req.draft_time_ms}")
                logger.info(f"Total target time: {req.target_time_ms}")
                total_time = time.time() - req.start_time
                logger.info(f"Total time: {total_time}")
                logger.info(f"TPS: {req.produced_token_count / total_time}")
                logger.info(f"Avg accepted tokens count: {req.accepted_token_count / req.iterations}")
                req.queue.put_nowait(None)
                return None

            req.input_ids = req.input_ids + target_output_ids
            req.fsm_state = target_output_states[-1] if len(target_output_states) > 0 else None
            return req

        # Generate all request_ids upfront
        target_request_ids = {req.id: self._calc_request_id() for req in requests}
        batch_request_ids = target_request_ids.values()
        st = time.time()
        tasks = [asyncio.create_task(
            call_target(req, target_request_ids[req.id], batch_request_ids)) 
            for req in requests]
        cont_reqs = await asyncio.gather(*tasks)
        logger.debug(f"all target reqs time", (time.time() - st) * 1000)
        cont_reqs = [req for req in cont_reqs if req is not None]
        return cont_reqs

    async def _draft_consumer(self, requests: List[SpecDecRequest]):
        """Consumes requests from the draft queue and fetches predictions from draft model.

        Args:
            requests (List[Request]): Requests to process

        Returns:
            List[Request]: Requests to continue.
        """
        @handle_request_exception
        async def call_draft(req, req_id, batch_request_ids):
            st = time.time()
            draft_ids = await self._call_draft(req_id, req, batch_request_ids)
            req.draft_time_ms += (time.time() - st) * 1000
            req.draft_ids = draft_ids
            req.draft_token_count += len(draft_ids)
        draft_request_ids = {req.id: self._calc_request_id() for req in requests}
        batch_request_ids = draft_request_ids.values()
        st = time.time()
        tasks = [
            asyncio.create_task(
                call_draft(req, draft_request_ids[req.id], batch_request_ids)) 
            for req in requests
        ]
        await asyncio.gather(*tasks)
        logger.debug(f"draft time for all reqs: ", (time.time() - st) * 1000)
        return requests


def set_briton_request_fields_from_model_input(model_input, briton_request):
    for model_input_key, briton_field in MODEL_INPUT_TO_BRITON_FIELD.items():
        if model_input_key in model_input:
            model_input_value = model_input[model_input_key]
            setattr(briton_request, briton_field, model_input_value)


async def _collect_text(async_text_iter):
    full_text = ""
    async for delta in async_text_iter:
        full_text += delta
    return full_text


def _openai_compatiblilty_check(model_metadata):
    if OPENAI_COMPATIBLE_TAG not in model_metadata:
        print(
            ("Warning: Defaulting to openai compatible interface, "
             "even though not indicated in config.")
        )
    return True


def _get_model_metadata_or_raise(model_metadata, key):
    if key not in model_metadata:
        raise ValueError(f"{key} is required in model_metadata")
    return model_metadata[key]


def _get_hf_token_or_none(secrets):
    try:
        return secrets.get("hf_access_token", None)
    except:  # noqa
        return None

