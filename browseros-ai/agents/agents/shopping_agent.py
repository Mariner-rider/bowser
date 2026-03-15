"""Shopping agent implementation scaffold."""

from agents.agent_base import AgentBase, TaskContext, TaskPlan, TaskRequest, TaskResult


class ShoppingAgent(AgentBase):
    def plan_task(self, task: TaskRequest, context: TaskContext) -> TaskPlan:
        return TaskPlan(steps=["search products", "compare prices", "rank options"], rationale=task.description)

    def call_tools(self, plan: TaskPlan, context: TaskContext) -> dict[str, object]:
        return {"comparisons": [], "steps": plan.steps}

    def execute_task(self, task: TaskRequest, context: TaskContext) -> TaskResult:
        return TaskResult(success=True, output="Shopping analysis scaffold complete", artifacts=self.call_tools(self.plan_task(task, context), context))
