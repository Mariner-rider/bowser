"""Service API layer for dashboard backend state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agent_monitor import AgentMonitor
from .event_logger import EventLogger
from .task_manager import TaskManager


@dataclass(slots=True)
class DashboardAPI:
    """Facade exposing monitoring dashboard operations."""

    task_manager: TaskManager
    agent_monitor: AgentMonitor
    event_logger: EventLogger
    learning_engine: Any | None = None

    def get_snapshot(self) -> dict[str, Any]:
        snapshot: dict[str, Any] = {
            "agents": self.agent_monitor.get_all_agents(),
            "tasks": self.task_manager.get_tasks(),
            "logs": self.event_logger.get_logs(limit=200),
        }
        if self.learning_engine is not None and hasattr(self.learning_engine, "get_feedback_summary"):
            snapshot["feedback"] = self.learning_engine.get_feedback_summary()
        return snapshot

    def pause_agent(self, agent_name: str) -> dict[str, Any]:
        self.agent_monitor.pause_agent(agent_name)
        self.event_logger.log("info", "dashboard", f"Paused agent {agent_name}")
        return {"ok": True, "agent": agent_name, "state": "paused"}

    def stop_agent(self, agent_name: str) -> dict[str, Any]:
        self.agent_monitor.stop_agent(agent_name)
        self.event_logger.log("warn", "dashboard", f"Stopped agent {agent_name}")
        return {"ok": True, "agent": agent_name, "state": "stopped"}

    def record_task_progress(self, task_id: str, progress: int, step: str | None = None) -> None:
        self.task_manager.update_progress(task_id, progress)
        if step:
            self.task_manager.add_automation_step(task_id, step)
            self.event_logger.log("info", "automation", f"Task {task_id} step", {"step": step})

    def submit_feedback(
        self,
        *,
        user_id: str,
        agent_name: str,
        task_kind: str,
        feedback: str,
        implicit: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Collect user feedback and return updated policy score."""
        if self.learning_engine is None:
            return {"ok": False, "error": "learning engine unavailable"}

        score = self.learning_engine.process_user_feedback(
            user_id=user_id,
            agent_name=agent_name,
            task_kind=task_kind,
            feedback=feedback,
            implicit=implicit,
        )
        self.event_logger.log(
            "info",
            "learning",
            "Feedback submitted",
            {"user_id": user_id, "agent_name": agent_name, "task_kind": task_kind, "score": score},
        )
        return {"ok": True, "policy_score": score, "summary": self.learning_engine.get_feedback_summary(user_id=user_id)}
