import lorem
from anthropic import AsyncAnthropic, Anthropic
from typing import Any, Dict, AsyncGenerator, Union, List
import asyncio

class AnthropicMockWrapper:
    def __init__(self, client: Union[Anthropic, AsyncAnthropic]):
        self.client = client
        self.is_test = isinstance(client, Anthropic) and client.api_key.startswith("TEST_")
        self.messages = self.Messages(self)
        self.completions = self.Completions(self)

    class Messages:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        async def create(self, *args: Any, **kwargs: Any) -> Any:
            if self.wrapper.is_test:
                max_tokens = kwargs.get("max_tokens", 100)
                model = kwargs.get("model", "claude-3-opus-20240229")
                messages = kwargs.get("messages", [])
                
                response_content = self.wrapper._generate_lorem_ipsum(max_tokens)
                
                class MockMessageResponse:
                    id = f"msg_{self.wrapper._generate_lorem_ipsum(8)}"
                    model = model
                    role = "assistant"
                    content = [{"type": "text", "text": response_content}]
                    stop_reason = "end_turn"
                    usage = {"input_tokens": 10, "output_tokens": max_tokens}

                return MockMessageResponse()
            
            if isinstance(self.wrapper.client, AsyncAnthropic):
                return await self.wrapper.client.messages.create(*args, **kwargs)
            else:
                return self.wrapper.client.messages.create(*args, **kwargs)

    class Completions:
        def __init__(self, wrapper):
            self.wrapper = wrapper

        async def create(self, *args: Any, **kwargs: Any) -> Any:
            if self.wrapper.is_test:
                max_tokens = kwargs.get("max_tokens_to_sample", 100)
                model = kwargs.get("model", "claude-2.1")
                prompt = kwargs.get("prompt", "")
                
                response_text = self.wrapper._generate_lorem_ipsum(max_tokens)
                
                class MockCompletionResponse:
                    completion = response_text
                    stop_reason = "length"
                    model = model

                return MockCompletionResponse()
            
            if isinstance(self.wrapper.client, AsyncAnthropic):
                return await self.wrapper.client.completions.create(*args, **kwargs)
            else:
                return self.wrapper.client.completions.create(*args, **kwargs)

    def _generate_lorem_ipsum(self, max_tokens: int) -> str:
        words = lorem.text().split()
        return " ".join(words[:max_tokens])

    def _generate_id(self, prefix: str, length: int = 8) -> str:
        return f"{prefix}_{self._generate_lorem_ipsum(length)}"