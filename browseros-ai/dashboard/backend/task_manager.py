"""Task tracking and control for dashboard operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class TaskManager:
    """Tracks task status, progress, and automation steps."""

    tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    def register_task(self, task_id: str, agent_name: str, description: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        self.tasks[task_id] = {
            "task_id": task_id,
            "agent_name": agent_name,
            "description": description,
            "status": "running",
            "progress": 0,
            "automation_steps": [],
            "created_at": timestamp,
            "updated_at": timestamp,
        }

    def update_progress(self, task_id: str, progress: int) -> None:
        task = self._require(task_id)
        task["progress"] = max(0, min(progress, 100))
        task["updated_at"] = datetime.now(timezone.utc).isoformat()

    def add_automation_step(self, task_id: str, step: str) -> None:
        task = self._require(task_id)
        task["automation_steps"].append(step)
        task["updated_at"] = datetime.now(timezone.utc).isoformat()

    def set_status(self, task_id: str, status: str) -> None:
        task = self._require(task_id)
        task["status"] = status
        task["updated_at"] = datetime.now(timezone.utc).isoformat()

    def get_tasks(self) -> list[dict[str, Any]]:
        return list(self.tasks.values())

    def _require(self, task_id: str) -> dict[str, Any]:
        if task_id not in self.tasks:
            raise KeyError(f"Task not found: {task_id}")
        return self.tasks[task_id]
