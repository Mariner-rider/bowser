"""Distributed inference coordinator for multi-node local AI mode."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .node_manager import NodeManager


@dataclass(slots=True)
class ClusterCoordinator:
    """Coordinates distributed workloads across registered nodes."""

    node_manager: NodeManager = field(default_factory=NodeManager)

    def dispatch(self, workload: dict[str, Any]) -> dict[str, Any]:
        nodes = self.node_manager.list_nodes()
        if not nodes:
            return {"dispatched": False, "reason": "no_nodes"}

        target = sorted(nodes, key=lambda n: float(n.get("gpu_memory_free_gb", 0.0)), reverse=True)[0]
        return {
            "dispatched": True,
            "node_id": target["node_id"],
            "workload": workload,
        }
