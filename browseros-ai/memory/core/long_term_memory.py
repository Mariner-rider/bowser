"""Long-term memory for durable key-value persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LongTermMemory:
    """Simple namespace-aware key-value store."""

    _storage: dict[str, dict[str, Any]] = field(default_factory=dict)

    def put(self, namespace: str, key: str, value: Any) -> None:
        self._storage.setdefault(namespace, {})[key] = value

    def get(self, namespace: str, key: str) -> Any:
        return self._storage.get(namespace, {}).get(key)

    def scan(self, namespace: str) -> dict[str, Any]:
        return dict(self._storage.get(namespace, {}))
