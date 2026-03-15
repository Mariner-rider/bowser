"""SDK contracts for third-party AI marketplace agents/tools."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentManifest:
    agent_id: str
    name: str
    version: str
    description: str
    capabilities: list[str]
    permissions: list[str] = field(default_factory=list)
    entrypoint: str = ""
    publisher_id: str = ""
    publisher_name: str = ""
    price_usd: float = 0.0
    public_listing: bool = True


@dataclass(slots=True)
class AgentExecutionRequest:
    agent_id: str
    input_payload: dict[str, Any]
    user_id: str | None = None


@dataclass(slots=True)
class AgentExecutionResponse:
    ok: bool
    output: dict[str, Any]
    error: str | None = None
