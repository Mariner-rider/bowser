"""Agent registry with specialized BrowserOS agent implementations."""

from __future__ import annotations

from dataclasses import dataclass

from .agent_base import (
    AgentBase,
    AgentCapability,
    AutomationEngine,
    LLMRouter,
    MemoryEngine,
    TaskContext,
    TaskPlan,
    TaskRequest,
    TaskResult,
)
from .task_planner import CAPABILITY_TO_NAMESPACE, TaskPlanner


class SpecializedAgent(AgentBase):
    """Reusable implementation used by concrete specialized agents."""

    def __init__(
        self,
        name: str,
        capability: AgentCapability,
        llm_router: LLMRouter,
        memory_engine: MemoryEngine,
        automation_engine: AutomationEngine,
        planner: TaskPlanner,
    ) -> None:
        super().__init__(name, capability, llm_router, memory_engine, automation_engine)
        self.planner = planner

    def plan_task(self, task: TaskRequest, context: TaskContext) -> TaskPlan:
        return self.planner.build_plan(task, context)

    def call_tools(self, plan: TaskPlan, context: TaskContext) -> dict[str, object]:
        automation = self.automation_engine.run(
            objective=f"Execute planned steps: {' | '.join(plan.steps)}",
            context=context,
        )
        return {"automation": automation, "steps_executed": len(plan.steps)}

    def execute_task(self, task: TaskRequest, context: TaskContext) -> TaskResult:
        plan = self.plan_task(task, context)
        memory_key = f"task:{context.task_id}:plan"
        namespace = CAPABILITY_TO_NAMESPACE[task.capability]
        self.memory_engine.remember(namespace, memory_key, plan.rationale)

        tool_output = self.call_tools(plan, context)
        prompt = (
            f"Agent {self.name} executed task '{task.description}'. "
            f"Plan rationale: {plan.rationale}. "
            f"Tool output: {tool_output}. Generate concise user-facing response."
        )
        llm_output = self.llm_router.generate(task=task.capability.value, prompt=prompt, context=context)
        self.memory_engine.remember(namespace, f"task:{context.task_id}:result", llm_output)

        return TaskResult(
            success=True,
            output=llm_output,
            artifacts={
                "plan": plan.steps,
                "tool_output": tool_output,
            },
        )


class ResearchAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("ResearchAgent", AgentCapability.RESEARCH, llm_router, memory_engine, automation_engine, planner)


class AutomationAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("AutomationAgent", AgentCapability.AUTOMATION, llm_router, memory_engine, automation_engine, planner)


class CodingAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("CodingAgent", AgentCapability.CODING, llm_router, memory_engine, automation_engine, planner)


class ShoppingAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("ShoppingAgent", AgentCapability.SHOPPING, llm_router, memory_engine, automation_engine, planner)


class SecurityAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("SecurityAgent", AgentCapability.SECURITY, llm_router, memory_engine, automation_engine, planner)


class ProductivityAgent(SpecializedAgent):
    def __init__(self, llm_router: LLMRouter, memory_engine: MemoryEngine, automation_engine: AutomationEngine, planner: TaskPlanner) -> None:
        super().__init__("ProductivityAgent", AgentCapability.PRODUCTIVITY, llm_router, memory_engine, automation_engine, planner)


@dataclass(slots=True)
class AgentRegistry:
    """Registry/factory for all supported specialized agents."""

    llm_router: LLMRouter
    memory_engine: MemoryEngine
    automation_engine: AutomationEngine
    planner: TaskPlanner

    def build(self) -> dict[AgentCapability, AgentBase]:
        agents: list[AgentBase] = [
            ResearchAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
            AutomationAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
            CodingAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
            ShoppingAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
            SecurityAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
            ProductivityAgent(self.llm_router, self.memory_engine, self.automation_engine, self.planner),
        ]
        return {agent.capability: agent for agent in agents}
