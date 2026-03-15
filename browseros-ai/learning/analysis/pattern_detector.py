"""Pattern detection helpers for learning engine analytics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PatternDetector:
    """Detects repeated interests, tasks, and workflow tendencies."""

    def top_terms(self, texts: list[str], *, limit: int = 5) -> list[str]:
        tokens: list[str] = []
        for text in texts:
            clean = ''.join(ch.lower() if ch.isalnum() or ch.isspace() else ' ' for ch in text)
            for token in clean.split():
                if len(token) > 2:
                    tokens.append(token)
        return [term for term, _ in Counter(tokens).most_common(limit)]

    def frequent_values(self, events: list[dict[str, Any]], key: str, *, limit: int = 5) -> list[str]:
        values = [str(item.get(key)) for item in events if item.get(key) is not None]
        return [value for value, _ in Counter(values).most_common(limit)]
