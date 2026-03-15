"""Natural language command parser for text/voice input."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .command_schema import StructuredCommand


@dataclass(slots=True)
class CommandParser:
    """Converts natural language into structured command objects."""

    _intent_patterns: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("research_topic", ("research", "find", "investigate", "look up")),
        ("coding_task", ("code", "implement", "build", "write")),
        ("automation_task", ("automate", "run workflow", "open and")),
        ("summarization", ("summarize", "summary of")),
    )

    def parse(self, user_input: str) -> StructuredCommand:
        normalized = " ".join(user_input.strip().split())
        if not normalized:
            raise ValueError("Command input cannot be empty")

        lowered = normalized.lower()
        for intent, prefixes in self._intent_patterns:
            for prefix in prefixes:
                if lowered.startswith(f"{prefix} "):
                    entity = normalized[len(prefix) :].strip()
                    return self._build_command(intent, entity, normalized)

        # Fallback defaults to research for unknown phrasing.
        return self._build_command("research_topic", normalized, normalized)

    def _build_command(self, intent: str, entity: str, raw_text: str) -> StructuredCommand:
        constraints = self._extract_constraints(raw_text)
        command = StructuredCommand(
            intent=intent,
            entity=entity,
            constraints=constraints,
            metadata={"raw_text": raw_text},
        )
        command.validate()
        return command

    def _extract_constraints(self, raw_text: str) -> list[str]:
        patterns = (
            r"\bwith ([^,.]+)",
            r"\bwithout ([^,.]+)",
            r"\busing ([^,.]+)",
        )
        constraints: list[str] = []
        lowered = raw_text.lower()
        for pattern in patterns:
            for match in re.findall(pattern, lowered):
                cleaned = match.strip()
                if cleaned and cleaned not in constraints:
                    constraints.append(cleaned)
        return constraints
