# wrapper.py

import asyncio
from typing import Any, Dict, List, Union, Optional, AsyncIterator
from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import (
    Message,
    MessageStream,
    MessageStreamEvent,
    Completion,
    MessageParam,
    ContentBlockParam,
    BatchCreateParams,
    BatchListParams,
)
import lorem

class AnthropicMockWrapper:
    def __init__(self, client: Union[Anthropic, AsyncAnthropic]):
        self.client = client
        self.is_test = client.api_key.startswith("TEST_")
        self.is_async = isinstance(client, AsyncAnthropic)
        self.messages = self.Messages(self)
        self.completions = self.Completions(self)
        self.beta = self.Beta(self)

    def _generate_lorem_ipsum(self, max_tokens: int) -> str:
        words = lorem.text().split()
        return " ".join(words[:max_tokens])

    def _generate_id(self, prefix: str) -> str:
        return f"{prefix}_{''.join([str(ord(c) % 10) for c in self._generate_lorem_ipsum(8)])}"

    async def _generate_lorem_ipsum_async(self, max_tokens: int) -> str:
        return await asyncio.to_thread(self._generate_lorem_ipsum, max_tokens)

    async def _generate_id_async(self, prefix: str) -> str:
        return f"{prefix}_{''.join([str(ord(c) % 10) for c in await self._generate_lorem_ipsum_async(8)])}"

    def _dispatch(self, sync_mock, async_mock, production):
        async def async_wrapper(*args, **kwargs):
            if self.is_test:
                return await async_mock(*args, **kwargs)
            return await production(*args, **kwargs)

        def sync_wrapper(*args, **kwargs):
            if self.is_test:
                return sync_mock(*args, **kwargs)
            return production(*args, **kwargs)

        return async_wrapper if self.is_async else sync_wrapper

    class Messages:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            self.create = wrapper._dispatch(
                self._create_mock_message_sync,
                self._create_mock_message_async,
                wrapper.client.messages.create
            )
            self.stream = wrapper._dispatch(
                self._stream_mock_message_sync,
                self._stream_mock_message_async,
                wrapper.client.messages.stream
            )

        def _create_mock_message_sync(self, model: str, max_tokens: int, messages: List[MessageParam], **kwargs) -> Message:
            response_content = self.wrapper._generate_lorem_ipsum(max_tokens)
            return Message(
                id=self.wrapper._generate_id("msg"),
                type="message",
                role="assistant",
                content=[{"type": "text", "text": response_content}],
                model=model,
                stop_reason="end_turn",
                usage={"input_tokens": 10, "output_tokens": max_tokens}
            )

        async def _create_mock_message_async(self, model: str, max_tokens: int, messages: List[MessageParam], **kwargs) -> Message:
            response_content = await self.wrapper._generate_lorem_ipsum_async(max_tokens)
            return Message(
                id=await self.wrapper._generate_id_async("msg"),
                type="message",
                role="assistant",
                content=[{"type": "text", "text": response_content}],
                model=model,
                stop_reason="end_turn",
                usage={"input_tokens": 10, "output_tokens": max_tokens}
            )

        def _stream_mock_message_sync(self, model: str, max_tokens: int, messages: List[MessageParam], **kwargs) -> MessageStream:
            response_content = self.wrapper._generate_lorem_ipsum(max_tokens)
            words = response_content.split()
            
            def generator():
                for word in words:
                    yield MessageStreamEvent(
                        type="content_block_delta",
                        index=0,
                        delta={"type": "text", "text": word + " "}
                    )
                yield MessageStreamEvent(
                    type="message_delta",
                    delta={"stop_reason": "end_turn"}
                )
                yield MessageStreamEvent(
                    type="message_stop",
                    message=Message(
                        id=self.wrapper._generate_id("msg"),
                        type="message",
                        role="assistant",
                        content=[{"type": "text", "text": response_content}],
                        model=model,
                        stop_reason="end_turn",
                        usage={"input_tokens": 10, "output_tokens": max_tokens}
                    )
                )

            return MessageStream(generator())

        async def _stream_mock_message_async(self, model: str, max_tokens: int, messages: List[MessageParam], **kwargs) -> AsyncIterator[MessageStreamEvent]:
            response_content = await self.wrapper._generate_lorem_ipsum_async(max_tokens)
            words = response_content.split()
            
            for word in words:
                yield MessageStreamEvent(
                    type="content_block_delta",
                    index=0,
                    delta={"type": "text", "text": word + " "}
                )
            yield MessageStreamEvent(
                type="message_delta",
                delta={"stop_reason": "end_turn"}
            )
            yield MessageStreamEvent(
                type="message_stop",
                message=Message(
                    id=await self.wrapper._generate_id_async("msg"),
                    type="message",
                    role="assistant",
                    content=[{"type": "text", "text": response_content}],
                    model=model,
                    stop_reason="end_turn",
                    usage={"input_tokens": 10, "output_tokens": max_tokens}
                )
            )

    class Completions:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            self.create = wrapper._dispatch(
                self._create_mock_completion_sync,
                self._create_mock_completion_async,
                wrapper.client.completions.create
            )

        def _create_mock_completion_sync(self, model: str, prompt: str, max_tokens_to_sample: int, **kwargs) -> Completion:
            response_text = self.wrapper._generate_lorem_ipsum(max_tokens_to_sample)
            return Completion(
                completion=response_text,
                stop_reason="max_tokens",
                model=model
            )

        async def _create_mock_completion_async(self, model: str, prompt: str, max_tokens_to_sample: int, **kwargs) -> Completion:
            response_text = await self.wrapper._generate_lorem_ipsum_async(max_tokens_to_sample)
            return Completion(
                completion=response_text,
                stop_reason="max_tokens",
                model=model
            )

    class Beta:
        def __init__(self, wrapper):
            self.wrapper = wrapper
            self.messages = self.Messages(wrapper)

        class Messages:
            def __init__(self, wrapper):
                self.wrapper = wrapper
                self.batches = self.Batches(wrapper)

            class Batches:
                def __init__(self, wrapper):
                    self.wrapper = wrapper
                    self.create = wrapper._dispatch(
                        self._create_mock_batch_sync,
                        self._create_mock_batch_async,
                        wrapper.client.beta.messages.batches.create
                    )
                    self.list = wrapper._dispatch(
                        self._list_mock_batches_sync,
                        self._list_mock_batches_async,
                        wrapper.client.beta.messages.batches.list
                    )
                    self.results = wrapper._dispatch(
                        self._get_mock_batch_results_sync,
                        self._get_mock_batch_results_async,
                        wrapper.client.beta.messages.batches.results
                    )

                def _create_mock_batch_sync(self, requests: List[BatchCreateParams], **kwargs) -> Dict[str, Any]:
                    return {
                        "id": self.wrapper._generate_id("batch"),
                        "processing_status": "created",
                        "created_at": "2023-01-01T00:00:00Z",
                    }

                async def _create_mock_batch_async(self, requests: List[BatchCreateParams], **kwargs) -> Dict[str, Any]:
                    return {
                        "id": await self.wrapper._generate_id_async("batch"),
                        "processing_status": "created",
                        "created_at": "2023-01-01T00:00:00Z",
                    }

                def _list_mock_batches_sync(self, **kwargs) -> Dict[str, Any]:
                    limit = kwargs.get("limit", 20)
                    batches = [
                        {
                            "id": self.wrapper._generate_id("batch"),
                            "processing_status": "completed",
                            "created_at": "2023-01-01T00:00:00Z",
                        }
                        for _ in range(limit)
                    ]
                    return {"data": batches, "has_more": False}

                async def _list_mock_batches_async(self, **kwargs) -> Dict[str, Any]:
                    limit = kwargs.get("limit", 20)
                    batches = [
                        {
                            "id": await self.wrapper._generate_id_async("batch"),
                            "processing_status": "completed",
                            "created_at": "2023-01-01T00:00:00Z",
                        }
                        for _ in range(limit)
                    ]
                    return {"data": batches, "has_more": False}

                def _get_mock_batch_results_sync(self, batch_id: str):
                    for _ in range(5):  # Simulate 5 results
                        yield {
                            "custom_id": self.wrapper._generate_id("custom"),
                            "result": {
                                "type": "succeeded",
                                "message": self.wrapper.messages._create_mock_message_sync(
                                    model="claude-3-opus-20240229",
                                    max_tokens=100,
                                    messages=[{"role": "user", "content": "Hello"}]
                                )
                            }
                        }

                async def _get_mock_batch_results_async(self, batch_id: str):
                    for _ in range(5):  # Simulate 5 results
                        yield {
                            "custom_id": await self.wrapper._generate_id_async("custom"),
                            "result": {
                                "type": "succeeded",
                                "message": await self.wrapper.messages._create_mock_message_async(
                                    model="claude-3-opus-20240229",
                                    max_tokens=100,
                                    messages=[{"role": "user", "content": "Hello"}]
                                )
                            }
                        }

    def with_options(self, **kwargs):
        if self.is_test:
            return self
        return self.client.with_options(**kwargs)

    def with_raw_response(self):
        if self.is_test:
            return self
        return self.client.with_raw_response()

    def with_streaming_response(self):
        if self.is_test:
            return self
        return self.client.with_streaming_response()