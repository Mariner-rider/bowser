"""Centralized event logging for dashboard monitoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

codex/extend-browseros-for-ai-browser-features-q722kc
try:
    from ...core.security.data_protector import SecureDataProtector, default_protector
except ImportError:  # pragma: no cover - script mode fallback
    from core.security.data_protector import SecureDataProtector, default_protector

=======
main

@dataclass(slots=True)
class EventLogger:
    """Stores structured logs for agents, tasks, and automation events."""

    logs: list[dict[str, Any]] = field(default_factory=list)
codex/extend-browseros-for-ai-browser-features-q722kc
    data_protector: SecureDataProtector = field(default_factory=default_protector)

    def log(self, level: str, source: str, message: str, payload: dict[str, Any] | None = None) -> None:
        safe_payload = self.data_protector.mask_payload(payload or {})
=======

    def log(self, level: str, source: str, message: str, payload: dict[str, Any] | None = None) -> None:
main
        self.logs.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level,
                "source": source,
                "message": message,
                "payload": safe_payload,
            }
        )

    def get_logs(self, *, limit: int = 100) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        return self.logs[-limit:]
