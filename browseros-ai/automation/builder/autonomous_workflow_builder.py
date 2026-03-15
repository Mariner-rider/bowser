"""Autonomous Workflow Builder for AI-powered visual automation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from ..core.automation_controller import AutomationController
from .workflow_schema import WorkflowDefinition, WorkflowNode


@dataclass(slots=True)
class AutonomousWorkflowBuilder:
    """Builds and executes user-designed visual workflows."""

    controller: AutomationController
    workflow_store: dict[str, WorkflowDefinition] = field(default_factory=dict)

    def create_workflow(self, name: str, nodes: list[WorkflowNode]) -> WorkflowDefinition:
        workflow = WorkflowDefinition(workflow_id=str(uuid4()), name=name, nodes=nodes)
        self.workflow_store[workflow.workflow_id] = workflow
        return workflow

    def execute_workflow(self, workflow_id: str) -> dict[str, Any]:
        workflow = self._require_workflow(workflow_id)
        return self.controller.manage_automation_task(task_name=workflow.name, steps=workflow.to_steps())

    def get_workflow(self, workflow_id: str) -> WorkflowDefinition:
        return self._require_workflow(workflow_id)

    def list_workflows(self) -> list[WorkflowDefinition]:
        return list(self.workflow_store.values())

    def market_research_template(self) -> WorkflowDefinition:
        """Template for: search -> collect links -> extract -> summarize -> report -> email."""

        nodes = [
            WorkflowNode("1", "Search Web", "navigate", {"url": "https://www.google.com"}),
            WorkflowNode("2", "Collect Top 10 Links", "scroll", {"amount": 800}),
            WorkflowNode("3", "Extract Data", "click", {"target": "results"}),
            WorkflowNode("4", "Summarize", "type", {"target": "#prompt", "text": "Summarize findings"}),
            WorkflowNode("5", "Generate Report", "click", {"target": "generate-report"}),
            WorkflowNode("6", "Email Report", "click", {"target": "email-report"}),
        ]
        return self.create_workflow("Market Research", nodes)

    def _require_workflow(self, workflow_id: str) -> WorkflowDefinition:
        if workflow_id not in self.workflow_store:
            raise KeyError(f"Workflow not found: {workflow_id}")
        return self.workflow_store[workflow_id]
