"""Memory manager orchestrating short-term, long-term, vector, and graph memory."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..brain.personal_knowledge_brain import KnowledgeItem, PersonalKnowledgeBrain
from ..graph.entity_extractor import EntityExtractor
from ..graph.knowledge_graph import KnowledgeGraph
from ..vector.embedding_service import EmbeddingService
from ..vector.vector_store import VectorStore
from .long_term_memory import LongTermMemory
from .short_term_memory import ShortTermMemory


@dataclass(slots=True)
class MemoryManager:
    """Unified memory interface compatible with agent memory protocol.

    Includes a tiny embedding cache to reduce repeated embed calls for identical input.
    """

    short_term: ShortTermMemory = field(default_factory=ShortTermMemory)
    long_term: LongTermMemory = field(default_factory=LongTermMemory)
    vector_store: VectorStore = field(default_factory=VectorStore)
    embedding_service: EmbeddingService = field(default_factory=EmbeddingService)
    knowledge_graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)
    entity_extractor: EntityExtractor = field(default_factory=EntityExtractor)
    knowledge_brain: PersonalKnowledgeBrain = field(default_factory=PersonalKnowledgeBrain)
    _embedding_cache: dict[str, list[float]] = field(default_factory=dict)
    _embedding_cache_order: list[str] = field(default_factory=list)
    embedding_cache_size: int = 256

    def store_memory(self, namespace: str, key: str, value: Any) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        self.long_term.put(namespace, key, value)
        self.short_term.store(
            {
                "namespace": namespace,
                "key": key,
                "value": value,
                "timestamp": timestamp,
            }
        )

        text = _to_text(value)
        embedding = self._embed_cached(text)
        self.vector_store.add_embedding(namespace, key, embedding, payload=value)

        entities = self.entity_extractor.extract(text)
        for entity in entities:
            self.knowledge_graph.add_entity(entity, {"namespace": namespace, "last_seen": timestamp})
            self.knowledge_graph.add_relationship(
                source=key,
                target=entity,
                relation="mentions",
                properties={"namespace": namespace},
            )

    def search_memory(self, namespace: str, query: str, *, top_k: int = 5) -> list[dict[str, Any]]:
        query_embedding = self._embed_cached(query)
        return self.vector_store.similarity_search(namespace, query_embedding, top_k=top_k)

    def retrieve_context(self, namespace: str, query: str, *, top_k: int = 5) -> dict[str, Any]:
        semantic = self.search_memory(namespace, query, top_k=top_k)
        graph = self.knowledge_graph.query_graph(query)
        recent = [item for item in self.short_term.recent(limit=top_k) if item["namespace"] == namespace]

        return {
            "semantic_matches": semantic,
            "graph": graph,
            "recent": recent,
        }

    def ingest_knowledge_item(
        self,
        topic: str,
        item_id: str,
        source_type: str,
        title: str,
        content: str,
        *,
        url: str | None = None,
        tags: list[str] | None = None,
    ) -> None:
        item = KnowledgeItem(
            item_id=item_id,
            source_type=source_type,
            title=title,
            content=content,
            url=url,
            tags=tags or [],
        )
        self.knowledge_brain.ingest_item(topic, item)

    def semantic_knowledge_search(self, topic: str, query: str, *, top_k: int = 5) -> list[dict[str, Any]]:
        return self.knowledge_brain.semantic_search(topic, query, top_k=top_k)

    def explore_topic_knowledge(self, topic: str) -> dict[str, Any]:
        return self.knowledge_brain.explore_topic(topic)

    def summarize_topic_knowledge(self, topic: str, *, max_items: int = 5) -> str:
        return self.knowledge_brain.automatic_summary(topic, max_items=max_items)

    # Compatibility helpers for agents.MemoryEngine protocol
    def remember(self, namespace: str, key: str, value: Any) -> None:
        self.store_memory(namespace, key, value)

    def recall(self, namespace: str, key: str) -> Any:
        return self.long_term.get(namespace, key)

    def _embed_cached(self, text: str) -> list[float]:
        if text in self._embedding_cache:
            return self._embedding_cache[text]

        embedding = self.embedding_service.embed(text)
        self._embedding_cache[text] = embedding
        self._embedding_cache_order.append(text)

        if len(self._embedding_cache_order) > self.embedding_cache_size:
            oldest = self._embedding_cache_order.pop(0)
            self._embedding_cache.pop(oldest, None)
        return embedding


def _to_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)
