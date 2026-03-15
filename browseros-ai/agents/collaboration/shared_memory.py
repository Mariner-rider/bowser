"""Shared memory for collaborative multi-agent task execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class SharedMemory:
    """Stores artifacts and context shared across collaborating agents."""

    task_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    task_context: dict[str, dict[str, Any]] = field(default_factory=dict)

    def store_context(self, collaboration_id: str, key: str, value: Any) -> None:
        self.task_context.setdefault(collaboration_id, {})[key] = value

    def get_context(self, collaboration_id: str) -> dict[str, Any]:
        return dict(self.task_context.get(collaboration_id, {}))

    def store_result(self, collaboration_id: str, agent_name: str, result: dict[str, Any]) -> None:
        self.task_results.setdefault(collaboration_id, {})[agent_name] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result,
        }

    def get_results(self, collaboration_id: str) -> dict[str, Any]:
        return dict(self.task_results.get(collaboration_id, {}))
