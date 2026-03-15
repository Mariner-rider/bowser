"""Agent runtime monitor with pause/stop controls."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class AgentMonitor:
    """Tracks active agents and supports lifecycle controls."""

    agents: dict[str, dict[str, Any]] = field(default_factory=dict)

    def set_agent_active(self, agent_name: str, active_task_id: str | None = None) -> None:
        self.agents[agent_name] = {
            "agent_name": agent_name,
            "state": "active",
            "active_task_id": active_task_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def pause_agent(self, agent_name: str) -> None:
        self._set_state(agent_name, "paused")

    def stop_agent(self, agent_name: str) -> None:
        self._set_state(agent_name, "stopped")

    def get_active_agents(self) -> list[dict[str, Any]]:
        return [agent for agent in self.agents.values() if agent["state"] in {"active", "paused"}]

    def get_all_agents(self) -> list[dict[str, Any]]:
        return list(self.agents.values())

    def _set_state(self, agent_name: str, state: str) -> None:
        if agent_name not in self.agents:
            self.agents[agent_name] = {
                "agent_name": agent_name,
                "state": state,
                "active_task_id": None,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            return

        self.agents[agent_name]["state"] = state
        self.agents[agent_name]["updated_at"] = datetime.now(timezone.utc).isoformat()
