"""Entity extraction utility for knowledge graph population."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EntityExtractor:
    """Very lightweight entity extractor based on capitalized tokens."""

    def extract(self, text: str) -> list[str]:
        entities: list[str] = []
        for token in text.replace("\n", " ").split(" "):
            token = token.strip(".,:;!?()[]{}\"'")
            if token and token[:1].isupper() and token not in entities:
                entities.append(token)
        return entities
