"""Text command handling pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from ..core.command_parser import CommandParser
from ..core.intent_router import IntentRouter


@dataclass(slots=True)
class TextInputHandler:
    """Parses natural language text and routes commands to AgentKernel."""

    command_parser: CommandParser
    intent_router: IntentRouter

    def handle_text_command(
        self,
        user_input: str,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        command = self.command_parser.parse(user_input)
        return self.intent_router.route(command, user_id=user_id, session_id=session_id, source="text")
