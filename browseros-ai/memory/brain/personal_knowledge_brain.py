"""Personal AI Knowledge Brain built on semantic memory + knowledge graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..graph.entity_extractor import EntityExtractor
from ..graph.knowledge_graph import KnowledgeGraph
from ..vector.embedding_service import EmbeddingService
from ..vector.vector_store import VectorStore


@dataclass(slots=True)
class KnowledgeItem:
    """Canonical item captured by the personal knowledge brain."""

    item_id: str
    source_type: str  # article | paper | github | summary | note | video | conversation
    title: str
    content: str
    url: str | None = None
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class PersonalKnowledgeBrain:
    """Structured personal research system beyond bookmarks/history."""

    embedding_service: EmbeddingService = field(default_factory=EmbeddingService)
    vector_store: VectorStore = field(default_factory=VectorStore)
    knowledge_graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)
    entity_extractor: EntityExtractor = field(default_factory=EntityExtractor)
    item_store: dict[str, KnowledgeItem] = field(default_factory=dict)

    def ingest_item(self, topic: str, item: KnowledgeItem) -> None:
        self.item_store[item.item_id] = item

        text = f"{item.title}\n{item.content}\n{' '.join(item.tags)}"
        embedding = self.embedding_service.embed(text)
        self.vector_store.add_embedding(topic, item.item_id, embedding, payload=item)

        self.knowledge_graph.add_entity(item.item_id, {
            "topic": topic,
            "type": item.source_type,
            "title": item.title,
            "url": item.url,
            "tags": item.tags,
            "created_at": item.created_at,
        })

        for entity in self.entity_extractor.extract(text):
            self.knowledge_graph.add_entity(entity, {"kind": "concept", "topic": topic})
            self.knowledge_graph.add_relationship(
                source=item.item_id,
                target=entity,
                relation="mentions",
                properties={"topic": topic},
            )

        for tag in item.tags:
            tag_node = f"tag:{tag.lower()}"
            self.knowledge_graph.add_entity(tag_node, {"kind": "tag", "topic": topic})
            self.knowledge_graph.add_relationship(
                source=item.item_id,
                target=tag_node,
                relation="tagged_with",
                properties={"topic": topic},
            )

    def semantic_search(self, topic: str, query: str, *, top_k: int = 5) -> list[dict[str, Any]]:
        query_embedding = self.embedding_service.embed(query)
        matches = self.vector_store.similarity_search(topic, query_embedding, top_k=top_k)

        results: list[dict[str, Any]] = []
        for match in matches:
            item = match["payload"]
            if isinstance(item, KnowledgeItem):
                results.append(
                    {
                        "score": round(match["score"], 4),
                        "item_id": item.item_id,
                        "source_type": item.source_type,
                        "title": item.title,
                        "url": item.url,
                        "tags": item.tags,
                    }
                )
        return results

    def link_topics(self, source_item_id: str, target_item_id: str, relation: str = "related_to") -> None:
        if source_item_id not in self.item_store or target_item_id not in self.item_store:
            raise KeyError("Both source and target items must exist before linking")

        self.knowledge_graph.add_relationship(
            source=source_item_id,
            target=target_item_id,
            relation=relation,
            properties={"linked_at": datetime.now(timezone.utc).isoformat()},
        )

    def explore_topic(self, topic: str) -> dict[str, Any]:
        node_matches = {
            node_id: data
            for node_id, data in self.knowledge_graph.entities.items()
            if str(data.get("topic", "")).lower() == topic.lower()
        }
        relationships = [
            rel
            for rel in self.knowledge_graph.relationships
            if str(rel.get("properties", {}).get("topic", "")).lower() == topic.lower()
        ]

        return {
            "topic": topic,
            "nodes": node_matches,
            "relationships": relationships,
            "stats": {
                "items": len([i for i in node_matches.values() if i.get("type")]),
                "concepts": len([i for i in node_matches.values() if i.get("kind") == "concept"]),
                "tags": len([i for i in node_matches.values() if i.get("kind") == "tag"]),
            },
        }

    def automatic_summary(self, topic: str, *, max_items: int = 5) -> str:
        items = [
            item
            for item in self.item_store.values()
            if self.knowledge_graph.entities.get(item.item_id, {}).get("topic", "").lower() == topic.lower()
        ][:max_items]

        if not items:
            return f"No knowledge captured yet for topic '{topic}'."

        titles = ", ".join(item.title for item in items)
        source_mix = ", ".join(sorted({item.source_type for item in items}))
        return (
            f"Topic '{topic}' summary: captured {len(items)} key resources ({source_mix}). "
            f"Primary focus areas include: {titles}."
        )
