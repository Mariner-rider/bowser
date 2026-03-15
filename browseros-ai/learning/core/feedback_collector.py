"""Feedback collector for explicit and implicit learning signals."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class FeedbackCollector:
    """Collects and stores interaction/feedback events locally.

    Uses bounded deques to prevent unbounded memory growth in long-running sessions.
    """

    max_events: int = 10_000
    interactions: deque[dict[str, Any]] = field(default_factory=deque)
    feedback_events: deque[dict[str, Any]] = field(default_factory=deque)

    def __post_init__(self) -> None:
        if self.interactions.maxlen != self.max_events:
            self.interactions = deque(self.interactions, maxlen=self.max_events)
        if self.feedback_events.maxlen != self.max_events:
            self.feedback_events = deque(self.feedback_events, maxlen=self.max_events)

    def collect_interaction(self, event: dict[str, Any]) -> None:
        self.interactions.append({"timestamp": datetime.now(timezone.utc).isoformat(), **event})

    def collect_feedback(self, event: dict[str, Any]) -> None:
        self.feedback_events.append({"timestamp": datetime.now(timezone.utc).isoformat(), **event})

    def get_user_interactions(self, user_id: str) -> list[dict[str, Any]]:
        return [item for item in self.interactions if item.get("user_id") == user_id]

    def get_user_feedback(self, user_id: str) -> list[dict[str, Any]]:
        return [item for item in self.feedback_events if item.get("user_id") == user_id]

    def summary(self, *, user_id: str | None = None) -> dict[str, int]:
        if user_id is None:
            return {
                "interactions": len(self.interactions),
                "feedback_events": len(self.feedback_events),
            }
        return {
            "interactions": len(self.get_user_interactions(user_id)),
            "feedback_events": len(self.get_user_feedback(user_id)),
        }

    def reset_user(self, user_id: str) -> None:
        self.interactions = deque((i for i in self.interactions if i.get("user_id") != user_id), maxlen=self.max_events)
        self.feedback_events = deque(
            (f for f in self.feedback_events if f.get("user_id") != user_id),
            maxlen=self.max_events,
        )
