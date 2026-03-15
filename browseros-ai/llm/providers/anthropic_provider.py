"""Anthropic provider adapter."""

from __future__ import annotations

from typing import Any, Iterator, Protocol

from ..base_provider import BaseProvider, ProviderConfig


class AnthropicClient(Protocol):
    def generate(self, model: str, prompt: str, **kwargs: Any) -> str: ...
    def stream(self, model: str, prompt: str, **kwargs: Any) -> Iterator[str]: ...
    def embed(self, model: str, text: str, **kwargs: Any) -> list[float]: ...


class AnthropicProvider(BaseProvider):
    def __init__(self, config: ProviderConfig, client: AnthropicClient) -> None:
        super().__init__(config)
        self.client = client

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.client.generate(self.config.model, prompt, **kwargs)

    def stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        yield from self.client.stream(self.config.model, prompt, **kwargs)

    def embed(self, text: str, **kwargs: Any) -> list[float]:
        return self.client.embed(self.config.model, text, **kwargs)
