"""Knowledge graph storage and query operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class KnowledgeGraph:
    """Simple property graph with entity and relationship support."""

    entities: dict[str, dict[str, Any]] = field(default_factory=dict)
    relationships: list[dict[str, Any]] = field(default_factory=list)

    def add_entity(self, entity_id: str, properties: dict[str, Any] | None = None) -> None:
        self.entities[entity_id] = properties or {}

    def add_relationship(
        self,
        source: str,
        target: str,
        relation: str,
        properties: dict[str, Any] | None = None,
    ) -> None:
        self.relationships.append(
            {
                "source": source,
                "target": target,
                "relation": relation,
                "properties": properties or {},
            }
        )

    def query_graph(self, query: str) -> dict[str, Any]:
        normalized = query.lower().strip()
        matched_entities = {
            entity_id: props
            for entity_id, props in self.entities.items()
            if normalized in entity_id.lower() or normalized in str(props).lower()
        }
        matched_relationships = [
            rel
            for rel in self.relationships
            if normalized in rel["source"].lower()
            or normalized in rel["target"].lower()
            or normalized in rel["relation"].lower()
            or normalized in str(rel["properties"]).lower()
        ]
        return {"entities": matched_entities, "relationships": matched_relationships}
