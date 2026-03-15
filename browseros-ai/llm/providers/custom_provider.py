"""Custom provider adapter for internal/private model backends."""

from __future__ import annotations

from typing import Any, Callable, Iterator

from ..base_provider import BaseProvider, ProviderConfig


class CustomProvider(BaseProvider):
    """Composable provider using injected callables."""

    def __init__(
        self,
        config: ProviderConfig,
        generate_fn: Callable[[str, dict[str, Any]], str],
        stream_fn: Callable[[str, dict[str, Any]], Iterator[str]],
        embed_fn: Callable[[str, dict[str, Any]], list[float]],
    ) -> None:
        super().__init__(config)
        self._generate_fn = generate_fn
        self._stream_fn = stream_fn
        self._embed_fn = embed_fn

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self._generate_fn(prompt, kwargs)

    def stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        yield from self._stream_fn(prompt, kwargs)

    def embed(self, text: str, **kwargs: Any) -> list[float]:
        return self._embed_fn(text, kwargs)
