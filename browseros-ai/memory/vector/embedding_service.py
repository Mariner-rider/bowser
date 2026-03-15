"""Embedding service used by the vector store for semantic memory search."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(slots=True)
class EmbeddingService:
    """Deterministic lightweight embedding implementation.

    This is a local fallback implementation intended to keep the module runnable
    without external embedding APIs.
    """

    dimensions: int = 16

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dimensions
        if not text:
            return vec

        for idx, char in enumerate(text.lower()):
            bucket = idx % self.dimensions
            vec[bucket] += (ord(char) % 97) / 100.0

        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]
