import traceback
from typing import AsyncIterable, Iterable, Optional

import aiohttp
import requests
from aiohttp import ClientTimeout
from betterproto import Casing
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from maitai._config import config
from maitai._maitai_client import MaitaiClient
from maitai._utils import __version__ as version
from maitai._utils import chat_completion_chunk_to_response
from maitai_common.utils.types import (
    AsyncChunkQueue,
    ChunkQueue,
    EvaluateCallback,
    QueueIterable,
)
from maitai_gen.chat import (
    ChatCompletionChunk,
    ChatCompletionParams,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatStorageRequest,
)
from maitai_gen.inference import InferenceStreamResponse
from maitai_gen.metric import RequestTimingMetric


class InferenceException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MaitaiConnectionError(ConnectionError):
    def __init__(self, msg: str):
        super().__init__(msg)


class InferenceWarning(Warning):
    def __init__(self, *args, **kwargs):
        pass


class Inference(MaitaiClient):
    _session = None

    def __init__(self):
        super().__init__()

    @classmethod
    def infer(
        cls, chat_request: ChatCompletionRequest, evaluate_callback, timeout
    ) -> Iterable[InferenceStreamResponse]:
        if evaluate_callback:
            q = ChunkQueue()
            cls.run_async(
                cls.send_inference_request_async(
                    chat_request,
                    chunk_queue=q,
                    timeout=timeout,
                    evaluation_callback=evaluate_callback,
                )
            )
            return QueueIterable(q, timeout=timeout)
        else:
            return cls.send_inference_request(chat_request, timeout)

    @classmethod
    async def infer_async(
        cls, chat_request: ChatCompletionRequest, evaluate_callback, timeout
    ) -> AsyncIterable[InferenceStreamResponse]:
        q = AsyncChunkQueue()
        cls.run_async(
            cls.send_inference_request_async(
                chat_request, async_chunk_queue=q, evaluation_callback=evaluate_callback
            )
        )
        return QueueIterable(q, timeout=timeout)

    @classmethod
    def store_chat_response(
        cls,
        session_id,
        reference_id,
        intent,
        application_ref_name,
        completion_params: ChatCompletionParams,
        chat_completion_response: Optional[ChatCompletionResponse],
        final_chunk: Optional[ChatCompletionChunk],
        content: str,
        timing: RequestTimingMetric,
        metadata: dict,
    ):
        inference_request = ChatCompletionRequest(
            application_ref_name=application_ref_name,
            session_id=session_id,
            reference_id=reference_id,
            action_type=intent,
            apply_corrections=False,
            evaluation_enabled=False,
            params=completion_params,
            auth_keys=config.auth_keys,
            metadata=metadata,
        )
        if final_chunk:
            chat_completion_response = chat_completion_chunk_to_response(
                final_chunk, content
            )
        chat_storage_request = ChatStorageRequest(
            chat_completion_request=inference_request,
            chat_completion_response=chat_completion_response,
            timing_metrics=timing,
        )
        cls.run_async(cls.send_storage_request_async(chat_storage_request))

    @classmethod
    def send_inference_request(
        cls, chat_request: ChatCompletionRequest, timeout
    ) -> Iterable[InferenceStreamResponse]:
        host = config.maitai_host
        url = f"{host}/chat/completions/serialized"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        session = cls.get_session()

        try:
            with session.post(
                url,
                headers=headers,
                data=chat_request.to_json(casing=Casing.SNAKE),
                stream=True,
                timeout=timeout,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        inference_response: InferenceStreamResponse = (
                            InferenceStreamResponse().from_json(line)
                        )
                        if not inference_response.keep_alive:
                            yield inference_response
        except requests.exceptions.RequestException as e:
            cls.log_error(str(e), url)
            raise MaitaiConnectionError(f"Failed to send inference request. Error: {e}")

    @classmethod
    async def send_inference_request_async(
        cls,
        chat_request: ChatCompletionRequest,
        chunk_queue: ChunkQueue = None,
        async_chunk_queue: AsyncChunkQueue = None,
        evaluation_callback: EvaluateCallback = None,
        timeout=None,
    ):
        host = config.maitai_host
        url = f"{host}/chat/completions/serialized"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                timeout=ClientTimeout(timeout) if timeout else None,
            ) as session:
                async with session.post(
                    url, headers=headers, data=chat_request.to_json(casing=Casing.SNAKE)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        cls.log_error(error_text, url)
                        exception = MaitaiConnectionError(
                            f"Failed to send inference request. Status code: {response.status}. Error: {error_text}"
                        )
                        if chunk_queue:
                            chunk_queue.put(exception)
                        if async_chunk_queue:
                            await async_chunk_queue.put(exception)
                        return
                    async for line in response.content:
                        if line:
                            inference_response: InferenceStreamResponse = (
                                InferenceStreamResponse().from_json(line)
                            )
                            if inference_response.keep_alive:
                                continue
                            if chunk_queue:
                                chunk_queue.put(inference_response)
                            if async_chunk_queue:
                                await async_chunk_queue.put(inference_response)
                            if (
                                inference_response.evaluate_response
                                and evaluation_callback
                            ):
                                try:
                                    evaluation_callback(
                                        inference_response.evaluate_response
                                    )
                                except:
                                    traceback.print_exc()
                    if chunk_queue:
                        chunk_queue.put(StopIteration())
                    if async_chunk_queue:
                        await async_chunk_queue.put(StopIteration())
        except Exception as e:
            exception = MaitaiConnectionError(
                f"Failed to send inference request: {str(e)}"
            )
            await cls.increment_error(str(e), url)
            if chunk_queue:
                chunk_queue.put(exception)
            if async_chunk_queue:
                await async_chunk_queue.put(exception)

    @classmethod
    async def send_storage_request_async(cls, chat_storage_request: ChatStorageRequest):
        host = config.maitai_host
        url = f"{host}/chat/completions/response"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            ) as session:
                return await session.put(
                    url,
                    headers=headers,
                    data=chat_storage_request.to_json(casing=Casing.SNAKE),
                )
        except Exception as e:
            await cls.increment_error(str(e), url)

    @classmethod
    def store_request_timing_data(cls, metric: RequestTimingMetric):
        cls.run_async(cls.send_request_timing_data(metric))

    @classmethod
    async def send_request_timing_data(cls, metric: RequestTimingMetric):
        host = config.maitai_host
        url = f"{host}/metrics/timing"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            ) as session:
                return await session.put(
                    url, headers=headers, data=metric.to_json(casing=Casing.SNAKE)
                )
        except:
            pass

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            retries = Retry(
                total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
            )
            cls._session.mount(
                "http://",
                HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=100),
            )
            cls._session.mount(
                "https://",
                HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=100),
            )
        return cls._session

    @classmethod
    def close_session(cls):
        if cls._session:
            cls._session.close()
            cls._session = None

    def __del__(self):
        self.close_session()
