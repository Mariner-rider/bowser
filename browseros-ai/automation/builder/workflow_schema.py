"""Schema definitions for visual autonomous workflow builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowNode:
    """Single visual workflow block (Zapier-style)."""

    node_id: str
    label: str
    action: str
    config: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkflowDefinition:
    """Complete workflow definition designed in the browser UI."""

    workflow_id: str
    name: str
    nodes: list[WorkflowNode]

    def to_steps(self) -> list[dict[str, Any]]:
        """Convert visual nodes to executor-ready steps."""

        steps: list[dict[str, Any]] = []
        for node in self.nodes:
            step = {"action": node.action, **node.config}
            steps.append(step)
        return steps
