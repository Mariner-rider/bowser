"""Registry for installed local AI models and metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelMetadata:
    model_id: str
    family: str
    size_billion_params: float
    backend: str
    path: str
    supports_streaming: bool = True
    quantization: str | None = None
    context_window: int = 8192


@dataclass(slots=True)
class ModelRegistry:
    """Tracks local models installed on device."""

    models: dict[str, ModelMetadata] = field(default_factory=dict)

    def register(self, metadata: ModelMetadata) -> None:
        self.models[metadata.model_id] = metadata

    def unregister(self, model_id: str) -> None:
        self.models.pop(model_id, None)

    def get(self, model_id: str) -> ModelMetadata | None:
        return self.models.get(model_id)

    def list_models(self) -> list[ModelMetadata]:
        return list(self.models.values())

    def disk_footprint(self) -> dict[str, Any]:
        # Lightweight estimate for scaffold mode.
        return {
            "models": len(self.models),
            "estimated_gb": round(sum(m.size_billion_params * 0.45 for m in self.models.values()), 2),
        }
