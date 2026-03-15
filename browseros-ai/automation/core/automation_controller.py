"""Automation controller to manage autonomous browser tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .workflow_runner import WorkflowRunner


@dataclass(slots=True)
class AutomationController:
    """Entry point that manages automation task lifecycle and logging."""

    workflow_runner: WorkflowRunner
    task_log: dict[str, dict[str, Any]] = field(default_factory=dict)

    def manage_automation_task(self, task_name: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        task_id = str(uuid4())
        started_at = datetime.now(timezone.utc).isoformat()
        record: dict[str, Any] = {
            "task_id": task_id,
            "task_name": task_name,
            "status": "running",
            "started_at": started_at,
            "ended_at": None,
            "actions": [],
            "error": None,
        }
        self.task_log[task_id] = record

        try:
            actions = self.workflow_runner.execute_workflow(steps)
            record["actions"] = actions
            record["status"] = "completed"
        except Exception as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
        finally:
            record["ended_at"] = datetime.now(timezone.utc).isoformat()

        return record

    def get_task_record(self, task_id: str) -> dict[str, Any] | None:
        return self.task_log.get(task_id)
