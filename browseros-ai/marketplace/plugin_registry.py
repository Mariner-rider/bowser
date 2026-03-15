"""Marketplace plugin registry for installable AI agents/apps."""

from __future__ import annotations

from dataclasses import dataclass, field

from .agent_sdk import AgentManifest


@dataclass(slots=True)
class PluginRegistry:
    """Registers, installs, and lists marketplace AI agents."""

    published: dict[str, AgentManifest] = field(default_factory=dict)
    installed: set[str] = field(default_factory=set)

    def publish(self, manifest: AgentManifest) -> None:
        self.published[manifest.agent_id] = manifest

    def install(self, agent_id: str) -> AgentManifest:
        if agent_id not in self.published:
            raise KeyError(f"Agent not found in marketplace: {agent_id}")
        self.installed.add(agent_id)
        return self.published[agent_id]

    def uninstall(self, agent_id: str) -> None:
        self.installed.discard(agent_id)

    def list_marketplace(self) -> list[AgentManifest]:
        return list(self.published.values())

    def list_installed(self) -> list[AgentManifest]:
        return [self.published[agent_id] for agent_id in sorted(self.installed) if agent_id in self.published]
