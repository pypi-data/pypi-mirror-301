import os
import time
import uuid
import warnings
from typing import Dict, Iterable, List, Mapping, Optional, Union

import httpx
import openai
import openai.types as openai_types
import openai.types.chat as openai_chat_types

import maitai
from maitai._config import config
from maitai._evaluator import Evaluator
from maitai._inference import (
    InferenceException,
    InferenceWarning,
    MaitaiConnectionError,
)
from maitai._types import (
    Body,
    Headers,
    MaitaiChunk,
    MaitaiCompletion,
    Query,
    ToolFunction,
)
from maitai._utils import (
    convert_open_ai_chat_completion_chunk,
    convert_openai_chat_completion,
    get_chat_completion_params,
    required_args,
)
from maitai.tools import Tools
from maitai_common.utils.proto_utils import openai_messages_to_proto
from maitai_common.utils.types import EvaluateCallback
from maitai_gen.chat import (
    ChatCompletionParams,
    ChatCompletionRequest,
    ChatMessage,
    ClientParams,
    EvaluationContentType,
)
from maitai_gen.config import InferenceLocations
from maitai_gen.inference import InferenceStreamResponse
from maitai_gen.metric import RequestTimingMetric

DEFAULT_MAX_RETRIES = 2


class Maitai:
    def __init__(
        self,
        *,
        maitai_api_key: Optional[str] = None,
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        cerebras_api_key: Optional[str] = None,
        organization: Optional[str] = None,
        project: Optional[str] = None,
        base_url: Union[str, httpx.URL, None] = None,
        timeout: Union[float, httpx.Timeout, None, openai.NotGiven] = openai.NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        http_client: Optional[httpx.Client] = None,
        _strict_response_validation: bool = False,
    ):
        if not maitai_api_key:
            maitai_api_key = os.environ.get("MAITAI_API_KEY")
        if maitai_api_key:
            config.initialize(maitai_api_key)
        if api_key:
            if not openai_api_key:
                openai_api_key = api_key
            if not groq_api_key:
                groq_api_key = api_key
            if not anthropic_api_key:
                anthropic_api_key = api_key
            if not cerebras_api_key:
                cerebras_api_key = api_key
        if openai_api_key:
            config.auth_keys.openai_api_key.key_value = openai_api_key
        if groq_api_key:
            config.auth_keys.groq_api_key.key_value = groq_api_key
        if anthropic_api_key:
            config.auth_keys.anthropic_api_key.key_value = anthropic_api_key
        if cerebras_api_key:
            config.auth_keys.cerebras_api_key.key_value = cerebras_api_key
        self._client = None
        if api_key or openai_api_key or os.environ.get("OPENAI_API_KEY"):
            self._client = openai.OpenAI(
                api_key=api_key or openai_api_key or os.environ.get("OPENAI_API_KEY"),
                organization=organization,
                project=project,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
                _strict_response_validation=_strict_response_validation,
            )
        client_params = None
        if base_url or default_headers or default_query:
            client_params = ClientParams(
                base_url=base_url or "",
                default_headers=default_headers or {},
                default_query=default_query or {},
            )
        self.chat = Chat(self._client, client_params)


class Chat:
    def __init__(self, client=None, client_params: ClientParams = None):
        self.completions = Completions(client, client_params)


class Completions:
    def __init__(
        self,
        client: Optional[openai.Client] = None,
        client_params: Optional[ClientParams] = None,
    ):
        self._client = client
        self._client_params = client_params or ClientParams()

    @required_args(
        ["intent", "application", "messages"],
        ["intent", "application_ref_name", "messages"],
        ["intent", "application", "messages", "model"],
        ["intent", "application_ref_name", "messages", "model"],
        ["intent", "application", "messages", "model", "stream"],
        ["intent", "application_ref_name", "messages", "model", "stream"],
    )
    def create(
        self,
        *,
        # Maitai Arguments
        user_id: str = "",
        session_id: Union[str, int] = None,
        reference_id: Union[str, int, None] = None,
        intent: str = None,
        action_type: str = None,  # DEPRECATED
        application_ref_name: str = None,  # DEPRECATED
        application: str = None,
        callback: Optional[EvaluateCallback] = None,
        server_side_inference: bool = None,
        evaluation_enabled: bool = None,
        apply_corrections: bool = None,
        context_retrieval_enabled: bool = None,
        context_query: str = "",
        return_request: bool = False,
        fallback_model: str = None,
        assistant: bool = False,
        metadata: dict = {},
        safe_mode: bool = None,
        # OpenAI Arguments
        messages: Iterable[openai_chat_types.ChatCompletionMessageParam],
        model: Union[str, openai_types.ChatModel, openai.NotGiven] = openai.NOT_GIVEN,
        frequency_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        function_call: Union[
            openai_chat_types.completion_create_params.FunctionCall, openai.NotGiven
        ] = openai.NOT_GIVEN,
        functions: Union[
            Iterable[openai_chat_types.completion_create_params.Function],
            openai.NotGiven,
        ] = openai.NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], openai.NotGiven] = openai.NOT_GIVEN,
        logprobs: Union[Optional[bool], openai.NotGiven] = openai.NOT_GIVEN,
        max_tokens: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        n: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        presence_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        response_format: Union[
            openai_chat_types.completion_create_params.ResponseFormat, openai.NotGiven
        ] = openai.NOT_GIVEN,
        seed: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        stop: Union[
            Union[Optional[str], List[str]], openai.NotGiven
        ] = openai.NOT_GIVEN,
        stream: Union[Optional[bool], openai.NotGiven] = openai.NOT_GIVEN,
        stream_options: Union[
            Optional[openai_chat_types.ChatCompletionStreamOptionsParam],
            openai.NotGiven,
        ] = openai.NOT_GIVEN,
        temperature: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        tool_choice: Union[
            openai_chat_types.ChatCompletionToolChoiceOptionParam, openai.NotGiven
        ] = openai.NOT_GIVEN,
        tools: Union[
            Tools,
            Iterable[Union[openai_chat_types.ChatCompletionToolParam, ToolFunction]],
            openai.NotGiven,
        ] = openai.NOT_GIVEN,
        top_logprobs: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        top_p: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        user: Union[str, openai.NotGiven] = openai.NOT_GIVEN,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, None, openai.NotGiven] = openai.NOT_GIVEN,
        parallel_tool_calls: Union[bool, openai.NotGiven] = openai.NOT_GIVEN,
    ) -> Union[MaitaiCompletion, Iterable[MaitaiChunk]]:
        retry_args = locals()
        timing = RequestTimingMetric(
            time_request_start=time.time(),
        )
        if not config.api_key:
            raise ValueError("Maitai API Key has not been set")
        if server_side_inference is False and apply_corrections is True:
            raise ValueError("server_side_inference must be true to apply_corrections")
        if apply_corrections is True and evaluation_enabled is False:
            raise ValueError("evaluations must be enabled to apply_corrections")
        if assistant is True:
            user_msgs = [True for msg in messages if msg["role"] == "user"]
            assistant_messages = [
                True for msg in messages if msg["role"] == "assistant"
            ]
            if len(user_msgs) != 1:
                raise ValueError(
                    "When assistant = True, exactly 1 user message is required"
                )
            if len(assistant_messages) > 0:
                raise ValueError(
                    "When assistant = True, no assistant messages are allowed"
                )
        if not session_id:
            session_id = str(uuid.uuid4())
        if not intent and action_type:
            intent = action_type
        if not application_ref_name and application:
            application_ref_name = application
        maitai_config = config.get_application_action_config(
            application_ref_name, intent
        )
        if server_side_inference is None:
            server_side_inference = (
                maitai_config.inference_location == InferenceLocations.SERVER
            )
        if evaluation_enabled is None:
            evaluation_enabled = maitai_config.evaluation_enabled
        if apply_corrections is None:
            apply_corrections = maitai_config.apply_corrections
        if model == openai.NOT_GIVEN:
            model = maitai_config.model
        if temperature == openai.NOT_GIVEN:
            temperature = maitai_config.temperature
        if safe_mode is None:
            safe_mode = maitai_config.safe_mode
        if stream == openai.NOT_GIVEN:
            stream = False
        if response_format == openai.NOT_GIVEN:
            response_format = {"type": "text"}
        if stop == openai.NOT_GIVEN and maitai_config.stop is not None:
            stop = maitai_config.stop
        if logprobs == openai.NOT_GIVEN:
            logprobs = maitai_config.logprobs
        if max_tokens == openai.NOT_GIVEN and maitai_config.max_tokens is not None:
            max_tokens = maitai_config.max_tokens
        if max_completion_tokens and max_completion_tokens != openai.NOT_GIVEN:
            max_tokens = max_completion_tokens
        if n == openai.NOT_GIVEN:
            n = maitai_config.n
        if frequency_penalty == openai.NOT_GIVEN:
            frequency_penalty = maitai_config.frequency_penalty
        if presence_penalty == openai.NOT_GIVEN:
            presence_penalty = maitai_config.presence_penalty
        if timeout == openai.NOT_GIVEN and maitai_config.timeout > 0:
            timeout = maitai_config.timeout
        if context_retrieval_enabled is None:
            context_retrieval_enabled = maitai_config.context_retrieval_enabled
        if fallback_model is None and maitai_config.fallback_model:
            fallback_model = maitai_config.fallback_model
        completion_params = get_chat_completion_params(
            messages=messages,
            model=model,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            n=n,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            stream=stream,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            parallel_tool_calls=parallel_tool_calls,
            extra_headers=extra_headers,
        )
        if server_side_inference:
            response_timeout = None
            if isinstance(timeout, float) or isinstance(timeout, int):
                response_timeout = timeout
            chat_request: ChatCompletionRequest = ChatCompletionRequest(
                application_ref_name=application_ref_name,
                session_id=session_id,
                reference_id=reference_id,
                action_type=intent,
                apply_corrections=apply_corrections,
                evaluation_enabled=evaluation_enabled,
                params=completion_params,
                return_evaluation=True if callback else False,
                context_retrieval_enabled=context_retrieval_enabled,
                context_query=context_query,
                return_request=return_request,
                fallback_model=fallback_model,
                user_id=user_id,
                assistant=assistant,
                auth_keys=config.auth_keys,
                metadata=metadata,
                safe_mode=safe_mode,
            )
            if self._client_params is not None:
                chat_request.client_params = self._client_params
            try:
                timing.time_pre_request = time.time()
                response = maitai.Inference.infer(
                    chat_request, callback, response_timeout
                )
                if stream:
                    if "self" in retry_args:
                        del retry_args["self"]
                    retry_args["server_side_inference"] = False
                    retry_args["model"] = model
                    retry_args["fallback_model"] = fallback_model
                    return _process_inference_stream(
                        response,
                        retry_args,
                        self.create,
                        timing,
                        includes_usage=(
                            stream_options.get("include_usage", False)
                            if stream_options and stream_options != openai.NOT_GIVEN
                            else False
                        ),
                    )
                # ChatCompletion only
                for resp in response:
                    if resp.warning:
                        warnings.warn(resp.warning, InferenceWarning)
                    if resp.error:
                        if "Unknown error occurred" in resp.error:
                            raise MaitaiConnectionError(resp.error)
                        raise InferenceException(resp.error)
                    timing.request_id = resp.chat_completion_response.request_id
                    timing.time_request_end = time.time()
                    maitai.Inference.store_request_timing_data(timing)
                    return MaitaiCompletion(resp.chat_completion_response)
                raise InferenceException("No data received")
            except MaitaiConnectionError as e:
                if "gpt" not in model and fallback_model and "gpt" in fallback_model:
                    model = fallback_model
                if "gpt" not in model:
                    raise e
                print("Maitai issue, retrying on client side")
                server_side_inference = False
        if not server_side_inference:
            if self._client is None:
                self._client = openai.OpenAI(
                    default_query=self._client_params.default_query or None,
                    default_headers=self._client_params.default_headers or None,
                    base_url=self._client_params.base_url or None,
                )
            response = self._client.chat.completions.create(
                messages=messages,
                model=model,
                frequency_penalty=frequency_penalty,
                function_call=function_call,
                functions=functions,
                logit_bias=logit_bias,
                logprobs=logprobs,
                max_tokens=max_tokens,
                n=n,
                presence_penalty=presence_penalty,
                response_format=response_format,
                seed=seed,
                stop=stop,
                stream=stream,
                stream_options=stream_options,
                temperature=temperature,
                tool_choice=tool_choice,
                tools=tools,
                top_logprobs=top_logprobs,
                top_p=top_p,
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                parallel_tool_calls=parallel_tool_calls,
            )
            if stream:
                return _process_openai_stream(
                    session_id,
                    reference_id,
                    intent,
                    application_ref_name,
                    messages,
                    response,
                    evaluation_enabled,
                    completion_params,
                    timing,
                    callback,
                    metadata,
                )
            else:
                timing.time_request_end = time.time()
                maitai_completion = convert_openai_chat_completion(response)
                proto_messages = openai_messages_to_proto(messages)
                proto_messages.append(
                    ChatMessage(
                        role="assistant",
                        content=maitai_completion.choices[0].message.content,
                    )
                )
                if evaluation_enabled:
                    maitai.Evaluator.evaluate(
                        session_id=session_id,
                        reference_id=reference_id,
                        intent=intent,
                        content_type=EvaluationContentType.MESSAGE,
                        content=proto_messages,
                        application_ref_name=application_ref_name,
                        callback=callback,
                        chat_completion_response=maitai_completion,
                        completion_params=completion_params,
                        timing=timing,
                        metadata=metadata,
                    )
                else:
                    maitai.Inference.store_chat_response(
                        session_id=session_id,
                        reference_id=reference_id,
                        intent=intent,
                        application_ref_name=application_ref_name,
                        chat_completion_response=maitai_completion,
                        completion_params=completion_params,
                        final_chunk=None,
                        content="",
                        timing=timing,
                        metadata=metadata,
                    )
                return MaitaiCompletion(maitai_completion)


def _process_openai_stream(
    session_id: Union[str, int],
    reference_id: Union[str, int, None],
    intent: str,
    application_ref_name: str,
    messages: Iterable[openai_chat_types.ChatCompletionMessageParam],
    stream: openai.Stream[openai_chat_types.ChatCompletionChunk],
    evaluation_enabled: bool,
    chat_completion_params: ChatCompletionParams,
    timing: RequestTimingMetric,
    callback: Optional[EvaluateCallback] = None,
    metadata: dict = {},
) -> Iterable[MaitaiChunk]:
    full_body = ""
    proto_messages = openai_messages_to_proto(messages)
    last_chunk = None
    for chunk in stream:
        if last_chunk is None:
            timing.time_first_chunk = time.time()
        maitai_chunk = convert_open_ai_chat_completion_chunk(chunk)
        if maitai_chunk.choices:
            last_chunk = maitai_chunk
            content = maitai_chunk.choices[0].delta.content
            if content is not None:
                full_body += content
        if maitai_chunk.usage and last_chunk is not None and not last_chunk.usage:
            last_chunk.usage = maitai_chunk.usage
        yield MaitaiChunk(maitai_chunk)
    timing.time_request_end = time.time()
    if evaluation_enabled:
        proto_messages.append(ChatMessage(role="assistant", content=full_body))
        Evaluator.evaluate(
            session_id=session_id,
            reference_id=reference_id,
            intent=intent,
            content_type=EvaluationContentType.MESSAGE,
            content=proto_messages,
            application_ref_name=application_ref_name,
            callback=callback,
            chat_completion_chunk=last_chunk,
            completion_params=chat_completion_params,
            timing=timing,
            metadata=metadata,
        )
    else:
        maitai.Inference.store_chat_response(
            session_id=session_id,
            reference_id=reference_id,
            intent=intent,
            application_ref_name=application_ref_name,
            completion_params=chat_completion_params,
            final_chunk=last_chunk,
            content=full_body,
            chat_completion_response=None,
            timing=timing,
            metadata=metadata,
        )


def _process_inference_stream(
    stream: Iterable[InferenceStreamResponse],
    retry_args: dict,
    retry_func,
    timing: RequestTimingMetric,
    includes_usage: bool = False,
) -> Iterable[MaitaiChunk]:
    first = True
    try:
        for infer_resp in stream:
            if infer_resp.warning:
                warnings.warn(infer_resp.warning, InferenceWarning)
            if infer_resp.error:
                raise InferenceException(infer_resp.error)
            chunk = infer_resp.chat_completion_chunk
            if chunk is not None:
                if first:
                    timing.time_first_chunk = time.time()
                    timing.request_id = chunk.request_id
                    first = False
                yield MaitaiChunk(chunk)
                if chunk.choices and chunk.choices[0].finish_reason:
                    timing.time_request_end = time.time()
                    maitai.Inference.store_request_timing_data(timing)
                if chunk.usage:
                    return
                if (
                    not includes_usage
                    and chunk.choices
                    and chunk.choices[0].finish_reason
                ):
                    return
    except MaitaiConnectionError as e:
        if "gpt" not in retry_args.get("model", "") and "gpt" in retry_args.get(
            "fallback_model", ""
        ):
            retry_args["model"] = retry_args["fallback_model"]
        if "gpt" in retry_args.get("model", ""):
            print("Maitai issue, retrying on client side")
            response = retry_func(**retry_args)
            for resp in response:
                yield resp
        else:
            raise e
