"""AgentKernel responsible for routing and lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .agent_base import AgentBase, AgentCapability, TaskContext, TaskRequest, TaskResult, TaskStatus


@dataclass(slots=True)
class TaskRecord:
    """Persistent task lifecycle snapshot maintained by kernel."""

    task_id: str
    description: str
    capability: AgentCapability
    status: TaskStatus
    created_at: str
    updated_at: str
    result: TaskResult | None = None
    error: str | None = None


@dataclass(slots=True)
class AgentKernel:
    """Coordinates agent routing and task execution lifecycle."""

    agents: dict[AgentCapability, AgentBase]
    tasks: dict[str, TaskRecord] = field(default_factory=dict)
    learning_engine: Any | None = None

    def receive_user_task(
        self,
        description: str,
        capability: AgentCapability,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
        constraints: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TaskRecord:
        task_id = str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        record = TaskRecord(
            task_id=task_id,
            description=description,
            capability=capability,
            status=TaskStatus.RECEIVED,
            created_at=timestamp,
            updated_at=timestamp,
        )
        self.tasks[task_id] = record
        self._learn_task_received(record, metadata or {})

        task_request = TaskRequest(
            description=description,
            capability=capability,
            constraints=constraints or [],
        )
        context = TaskContext(
            task_id=task_id,
            user_id=user_id,
            session_id=session_id,
            trace_id=str(uuid4()),
            metadata=metadata or {},
        )
        self.manage_task_execution(task_request, context)
        return self.tasks[task_id]

    def route_task(self, capability: AgentCapability) -> AgentBase:
        if capability not in self.agents:
            raise ValueError(f"No agent registered for capability={capability.value}")
        return self.agents[capability]

    def manage_task_execution(self, task: TaskRequest, context: TaskContext) -> None:
        record = self.tasks[context.task_id]
        try:
            record.status = TaskStatus.PLANNED
            record.updated_at = datetime.now(timezone.utc).isoformat()

            agent = self.route_task(task.capability)

            record.status = TaskStatus.RUNNING
            record.updated_at = datetime.now(timezone.utc).isoformat()

            result = agent.execute_task(task, context)
            record.result = result
            record.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
            record.updated_at = datetime.now(timezone.utc).isoformat()
            self._learn_task_outcome(record)
        except Exception as exc:  # defensive guardrail for lifecycle integrity
            record.status = TaskStatus.FAILED
            record.error = str(exc)
            record.updated_at = datetime.now(timezone.utc).isoformat()
            self._learn_task_outcome(record)

    def _learn_task_received(self, record: TaskRecord, metadata: dict[str, Any]) -> None:
        if self.learning_engine is None:
            return
        self.learning_engine.collect_interaction_data(
            {
                "user_id": metadata.get("user_id"),
                "task_id": record.task_id,
                "task_kind": record.capability.value,
                "description": record.description,
                "status": record.status.value,
            }
        )

    def _learn_task_outcome(self, record: TaskRecord) -> None:
        if self.learning_engine is None:
            return
        user_id = None
        if record.result and isinstance(record.result.artifacts, dict):
            user_id = str(record.result.artifacts.get("user_id", "")) or None
        self.learning_engine.update_from_outcome(
            user_id=user_id or "anonymous",
            agent_name=record.capability.value,
            task_kind=record.capability.value,
            status=record.status.value,
        )

    def get_task(self, task_id: str) -> TaskRecord | None:
        return self.tasks.get(task_id)
