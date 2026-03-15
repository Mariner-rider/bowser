"""Short-term memory optimized for session-scoped, recency-focused retrieval."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ShortTermMemory:
    """In-memory bounded buffer for recent interactions."""

    max_items: int = 100
    _entries: deque[dict[str, Any]] = field(default_factory=deque)

    def store(self, item: dict[str, Any]) -> None:
        self._entries.append(item)
        while len(self._entries) > self.max_items:
            self._entries.popleft()

    def recent(self, limit: int = 10) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        return list(self._entries)[-limit:]
