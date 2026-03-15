"""Routes structured commands to AgentKernel tasks."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from ...agents.agent_base import AgentCapability
    from ...agents.agent_kernel import AgentKernel, TaskRecord
except ImportError:  # pragma: no cover - script mode fallback
    from agents.agent_base import AgentCapability
    from agents.agent_kernel import AgentKernel, TaskRecord
from .command_schema import StructuredCommand


INTENT_TO_CAPABILITY: dict[str, AgentCapability] = {
    "research_topic": AgentCapability.RESEARCH,
    "coding_task": AgentCapability.CODING,
    "automation_task": AgentCapability.AUTOMATION,
    "shopping_task": AgentCapability.SHOPPING,
    "security_task": AgentCapability.SECURITY,
    "productivity_task": AgentCapability.PRODUCTIVITY,
    "summarization": AgentCapability.RESEARCH,
}


@dataclass(slots=True)
class IntentRouter:
    """Maps command intents into AgentKernel executions."""

    agent_kernel: AgentKernel

    def route(
        self,
        command: StructuredCommand,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
        source: str = "text",
    ) -> TaskRecord:
        command.validate()
        capability = INTENT_TO_CAPABILITY.get(command.intent, AgentCapability.RESEARCH)
        description = f"{command.intent}: {command.entity}"
        return self.agent_kernel.receive_user_task(
            description=description,
            capability=capability,
            user_id=user_id,
            session_id=session_id,
            constraints=command.constraints,
            metadata={"intent": command.intent, "source": source, "command": command.to_dict(), **command.metadata},
        )
