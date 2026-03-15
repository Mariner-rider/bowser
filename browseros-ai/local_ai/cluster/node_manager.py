"""Node manager for distributed local AI cluster mode."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class NodeManager:
    """Registers and monitors local/remote compute nodes."""

    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)

    def register_node(self, node_id: str, capabilities: dict[str, Any]) -> None:
        self.nodes[node_id] = capabilities

    def remove_node(self, node_id: str) -> None:
        self.nodes.pop(node_id, None)

    def list_nodes(self) -> list[dict[str, Any]]:
        return [{"node_id": node_id, **caps} for node_id, caps in self.nodes.items()]
