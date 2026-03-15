"""Multi-step workflow runner for autonomous automation tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..actions.action_executor import ActionExecutor
from ..page.page_interpreter import PageInterpreter


@dataclass(slots=True)
class WorkflowRunner:
    """Executes interpreted workflow steps using ActionExecutor."""

    interpreter: PageInterpreter
    executor: ActionExecutor

    def execute_workflow(self, steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for raw_step in steps:
            step = self.interpreter.interpret_step(raw_step)
            action = step["action"]

            if action == "navigate":
                self.executor.navigate_url(step["url"])
            elif action == "click":
                self.executor.click_element(step["selector"])
            elif action == "type":
                self.executor.type_text(step["selector"], step["text"])
            elif action == "scroll":
                self.executor.scroll_page(int(step["amount"]))
            else:
                raise ValueError(f"Unsupported workflow action: {action}")

        return self.executor.get_action_log()
