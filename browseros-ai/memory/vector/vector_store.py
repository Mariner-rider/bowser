"""Vector storage and similarity search for semantic memory retrieval."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import math


@dataclass(slots=True)
class VectorStore:
    """In-memory vector index supporting cosine similarity lookup."""

    _index: list[dict[str, Any]] = field(default_factory=list)

    def add_embedding(self, namespace: str, key: str, embedding: list[float], payload: Any) -> None:
        self._index.append(
            {
                "namespace": namespace,
                "key": key,
                "embedding": embedding,
                "payload": payload,
            }
        )

    def similarity_search(
        self,
        namespace: str,
        query_embedding: list[float],
        *,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        scored: list[tuple[float, dict[str, Any]]] = []
        for item in self._index:
            if item["namespace"] != namespace:
                continue
            score = _cosine_similarity(query_embedding, item["embedding"])
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "score": score,
                "key": item["key"],
                "payload": item["payload"],
            }
            for score, item in scored[:top_k]
        ]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding dimensions do not match")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
