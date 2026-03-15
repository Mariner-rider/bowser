"""Run a local end-to-end BrowserOS AI pipeline without external services."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.agent_base import AgentCapability, TaskContext
from agents.agent_kernel import AgentKernel
from agents.agents.automation_agent import AutomationAgent
from agents.agents.coding_agent import CodingAgent
from agents.agents.research_agent import ResearchAgent
from automation.actions.action_executor import ActionExecutor
from automation.core.automation_controller import AutomationController
from automation.core.workflow_runner import WorkflowRunner
from automation.page.element_locator import ElementLocator
from automation.page.page_interpreter import PageInterpreter
from core.chromium_bridge.browseros_runtime import BrowserOSRuntime
from core.chromium_bridge.runtime_session import RuntimeBrowserSession
from interface.core.command_parser import CommandParser
from interface.core.intent_router import IntentRouter


class LocalMemory:
    def __init__(self) -> None:
        self._storage: dict[tuple[str, str], object] = {}

    def remember(self, namespace: str, key: str, value: object) -> None:
        self._storage[(namespace, key)] = value

    def recall(self, namespace: str, key: str) -> object:
        return self._storage.get((namespace, key))


class LocalLLM:
    def generate(self, task: str, prompt: str, context: TaskContext) -> str:
        return f"[{task}] {prompt[:120]}"


class LocalAutomation:
    def __init__(self, controller: AutomationController) -> None:
        self.controller = controller

    def run(self, objective: str, context: TaskContext) -> dict[str, object]:
        steps = [
            {"action": "navigate", "url": "https://example.com"},
            {"action": "click", "selector": "#search"},
            {"action": "type", "selector": "#search", "text": objective},
            {"action": "scroll", "amount": 300},
        ]
        return self.controller.manage_automation_task(task_name="e2e", steps=steps)


def build_kernel() -> AgentKernel:
    runtime = BrowserOSRuntime()
    session = RuntimeBrowserSession(runtime)
    executor = ActionExecutor(session=session)
    runner = WorkflowRunner(interpreter=PageInterpreter(locator=ElementLocator()), executor=executor)
    automation = LocalAutomation(AutomationController(workflow_runner=runner))

    llm = LocalLLM()
    memory = LocalMemory()

    agents = {
        AgentCapability.RESEARCH: ResearchAgent("research", AgentCapability.RESEARCH, llm, memory, automation),
        AgentCapability.CODING: CodingAgent("coding", AgentCapability.CODING, llm, memory, automation),
        AgentCapability.AUTOMATION: AutomationAgent("automation", AgentCapability.AUTOMATION, llm, memory, automation),
    }
    return AgentKernel(agents=agents)


def main() -> int:
    kernel = build_kernel()
    parser = CommandParser()
    router = IntentRouter(agent_kernel=kernel)

    command = parser.parse("automate open and summarize with quick mode")
    task = router.route(command, user_id="local-user", session_id="local-session", source="cli")

    output = {
        "task_id": task.task_id,
        "status": task.status.value,
        "result": task.result.output if task.result else None,
        "artifacts": task.result.artifacts if task.result else None,
    }
    print(json.dumps(output, indent=2))
    return 0 if task.status.value == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
