"""Trusted model downloader abstraction for local AI engines."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .model_registry import ModelMetadata


@dataclass(slots=True)
class ModelDownloader:
    """Downloads/models sync from trusted repositories (scaffold implementation)."""

    trusted_repositories: list[str] = field(
        default_factory=lambda: [
            "https://huggingface.co",
            "https://models.example.local",
        ]
    )

    def download(
        self,
        *,
        model_id: str,
        family: str,
        backend: str,
        source_url: str,
        target_dir: str,
        size_billion_params: float,
        quantization: str | None = None,
    ) -> ModelMetadata:
        if not any(source_url.startswith(repo) for repo in self.trusted_repositories):
            raise ValueError("Model source is not in trusted repositories")

        path = Path(target_dir) / model_id
        path.parent.mkdir(parents=True, exist_ok=True)
        # Placeholder artifact to keep local flow testable without network.
        path.write_text(f"model:{model_id}\nbackend:{backend}\nsource:{source_url}\n", encoding="utf-8")

        return ModelMetadata(
            model_id=model_id,
            family=family,
            size_billion_params=size_billion_params,
            backend=backend,
            path=str(path),
            quantization=quantization,
        )

    def update(self, model_id: str) -> dict[str, Any]:
        return {"model_id": model_id, "updated": True}
