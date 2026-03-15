"""Research agent implementation scaffold."""

from agents.agent_base import AgentBase, TaskContext, TaskPlan, TaskRequest, TaskResult


class ResearchAgent(AgentBase):
    def plan_task(self, task: TaskRequest, context: TaskContext) -> TaskPlan:
        return TaskPlan(steps=["collect sources", "summarize findings"], rationale=task.description)

    def call_tools(self, plan: TaskPlan, context: TaskContext) -> dict[str, object]:
        return {"sources": [], "notes": plan.steps}

    def execute_task(self, task: TaskRequest, context: TaskContext) -> TaskResult:
        plan = self.plan_task(task, context)
        tool_data = self.call_tools(plan, context)
        return TaskResult(success=True, output="Research plan completed", artifacts=tool_data)
