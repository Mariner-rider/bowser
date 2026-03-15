"""Canonical command schema for AI command interface."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class StructuredCommand:
    """Normalized command payload produced by command parsers.

    Example dictionary payload:
    {
      "intent": "research_topic",
      "entity": "AI agents"
    }
    """

    intent: str
    entity: str
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Ensure the command has a minimal valid shape."""

        if not self.intent.strip():
            raise ValueError("StructuredCommand.intent cannot be empty")
        if not self.entity.strip():
            raise ValueError("StructuredCommand.entity cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        """Serialize command for logging, APIs, and transport."""

        return asdict(self)
