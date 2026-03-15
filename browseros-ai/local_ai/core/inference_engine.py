"""Local inference engine adapter layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from ..models.model_registry import ModelMetadata


@dataclass(slots=True)
class InferenceEngine:
    """Runs local inference and streaming for local model backends."""

    backend_name: str

    def generate(self, model: ModelMetadata, prompt: str) -> str:
        return f"[{self.backend_name}:{model.model_id}] {prompt[:240]}"

    def stream(self, model: ModelMetadata, prompt: str) -> Iterator[str]:
        text = self.generate(model, prompt)
        for idx in range(0, len(text), 40):
            yield text[idx : idx + 40]
