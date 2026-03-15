"""Marketplace plugin registry for installable AI agents/apps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .agent_sdk import AgentManifest


@dataclass(slots=True)
class PluginRegistry:
    """Registers, installs, and lists marketplace AI agents."""

    published: dict[str, AgentManifest] = field(default_factory=dict)
    installed: set[str] = field(default_factory=set)

    def publish(self, manifest: AgentManifest) -> None:
        self.published[manifest.agent_id] = manifest

    def publish_from_public_submission(self, submission: dict[str, Any]) -> AgentManifest:
        """Public app-store-like submission endpoint for community agents."""
        required = ["agent_id", "name", "version", "description", "capabilities", "publisher_id", "publisher_name"]
        missing = [k for k in required if not submission.get(k)]
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")

        manifest = AgentManifest(
            agent_id=str(submission["agent_id"]),
            name=str(submission["name"]),
            version=str(submission["version"]),
            description=str(submission["description"]),
            capabilities=list(submission["capabilities"]),
            permissions=list(submission.get("permissions", [])),
            entrypoint=str(submission.get("entrypoint", "")),
            publisher_id=str(submission["publisher_id"]),
            publisher_name=str(submission["publisher_name"]),
            price_usd=float(submission.get("price_usd", 0.0)),
            public_listing=bool(submission.get("public_listing", True)),
        )
        self.publish(manifest)
        return manifest

    def install(self, agent_id: str) -> AgentManifest:
        if agent_id not in self.published:
            raise KeyError(f"Agent not found in marketplace: {agent_id}")
        self.installed.add(agent_id)
        return self.published[agent_id]

    def uninstall(self, agent_id: str) -> None:
        self.installed.discard(agent_id)

    def list_marketplace(self) -> list[AgentManifest]:
        return list(self.published.values())

    def list_public_marketplace(self) -> list[AgentManifest]:
        return [m for m in self.published.values() if m.public_listing]

    def list_installed(self) -> list[AgentManifest]:
        return [self.published[agent_id] for agent_id in sorted(self.installed) if agent_id in self.published]
