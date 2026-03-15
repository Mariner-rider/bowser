"""Base provider abstractions for the BrowserOS universal LLM router."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass(slots=True)
class ProviderConfig:
    """Runtime provider configuration."""

    name: str
    model: str
    timeout_seconds: int = 30
    options: dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    """Abstract provider contract for text generation and embeddings."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Return a complete generation for the provided prompt."""

    @abstractmethod
    def stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """Yield generated chunks for streaming responses."""

    @abstractmethod
    def embed(self, text: str, **kwargs: Any) -> list[float]:
        """Return embedding vector for text."""
