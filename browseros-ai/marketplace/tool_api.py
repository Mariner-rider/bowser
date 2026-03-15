"""Tool API surface exposed to marketplace agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ToolAPI(Protocol):
    def run_tool(self, tool_name: str, payload: dict) -> dict: ...


@dataclass(slots=True)
class LocalToolAPI:
    """Minimal tool API implementation for extension-safe execution."""

    def run_tool(self, tool_name: str, payload: dict) -> dict:
        return {"tool": tool_name, "status": "ok", "payload": payload}
