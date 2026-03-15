"""Speech-to-text abstraction for voice command ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SpeechEngine(Protocol):
    def transcribe(self, audio_bytes: bytes, *, locale: str | None = None) -> str:
        ...


@dataclass(slots=True)
class SpeechToText:
    """Adapter around pluggable speech transcription engines."""

    engine: SpeechEngine

    def transcribe(self, audio_bytes: bytes, *, locale: str | None = None) -> str:
        return self.engine.transcribe(audio_bytes, locale=locale)
