"""Task planning utilities for converting natural language goals into steps."""

from __future__ import annotations

from dataclasses import dataclass

from .agent_base import AgentCapability, TaskContext, TaskPlan, TaskRequest


@dataclass(slots=True)
class TaskPlanner:
    """Lightweight planner that can be upgraded to graph/workflow planning later."""

    def build_plan(self, task: TaskRequest, context: TaskContext) -> TaskPlan:
        constraints = ", ".join(task.constraints) if task.constraints else "none"
        steps = [
            f"Understand task objective for {task.capability.value}",
            "Collect context from memory and active session",
            "Generate actionable approach using LLM router",
            "Execute tool actions and validate outcomes",
            "Persist summary and artifacts back to memory",
        ]
        rationale = (
            f"Plan for task={context.task_id} capability={task.capability.value}; "
            f"constraints={constraints}"
        )
        return TaskPlan(steps=steps, rationale=rationale)


CAPABILITY_TO_NAMESPACE: dict[AgentCapability, str] = {
    AgentCapability.RESEARCH: "research",
    AgentCapability.AUTOMATION: "automation",
    AgentCapability.CODING: "coding",
    AgentCapability.SHOPPING: "shopping",
    AgentCapability.SECURITY: "security",
    AgentCapability.PRODUCTIVITY: "productivity",
}
