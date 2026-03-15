"""In-memory communication bus for multi-agent collaboration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class AgentCommunicationBus:
    """Tracks inter-agent messages for coordination and debugging."""

    messages: list[dict[str, Any]] = field(default_factory=list)

    def publish(
        self,
        collaboration_id: str,
        *,
        sender: str,
        recipient: str,
        message_type: str,
        payload: dict[str, Any],
    ) -> None:
        self.messages.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "collaboration_id": collaboration_id,
                "sender": sender,
                "recipient": recipient,
                "message_type": message_type,
                "payload": payload,
            }
        )

    def get_messages(self, collaboration_id: str) -> list[dict[str, Any]]:
        return [msg for msg in self.messages if msg["collaboration_id"] == collaboration_id]
