"""Centralized event logging for dashboard monitoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class EventLogger:
    """Stores structured logs for agents, tasks, and automation events."""

    logs: list[dict[str, Any]] = field(default_factory=list)

    def log(self, level: str, source: str, message: str, payload: dict[str, Any] | None = None) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level,
                "source": source,
                "message": message,
                "payload": payload or {},
            }
        )

    def get_logs(self, *, limit: int = 100) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        return self.logs[-limit:]
