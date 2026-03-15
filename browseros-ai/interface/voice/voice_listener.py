"""Voice listener pipeline for command parsing and routing."""

from __future__ import annotations

from dataclasses import dataclass

from ..core.command_parser import CommandParser
from ..core.intent_router import IntentRouter
from .speech_to_text import SpeechToText


@dataclass(slots=True)
class VoiceListener:
    """Converts audio input into commands and routes to AgentKernel."""

    speech_to_text: SpeechToText
    command_parser: CommandParser
    intent_router: IntentRouter

    def handle_audio_command(
        self,
        audio_bytes: bytes,
        *,
        locale: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        text = self.speech_to_text.transcribe(audio_bytes, locale=locale)
        command = self.command_parser.parse(text)
        return self.intent_router.route(command, user_id=user_id, session_id=session_id, source="voice")
