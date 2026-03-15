"""Autonomous multi-agent orchestrator for parallel collaborative execution."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..agent_base import AgentCapability
from ..agent_kernel import AgentKernel, TaskRecord
from .agent_communication_bus import AgentCommunicationBus
from .shared_memory import SharedMemory
from .task_scheduler import ScheduledAgentTask, TaskScheduler


CAPABILITY_MAP: dict[str, AgentCapability] = {
    "research": AgentCapability.RESEARCH,
    "coding": AgentCapability.CODING,
    "automation": AgentCapability.AUTOMATION,
    "security": AgentCapability.SECURITY,
    "productivity": AgentCapability.PRODUCTIVITY,
    "shopping": AgentCapability.SHOPPING,
}


@dataclass(slots=True)
class CollaborationResult:
    collaboration_id: str
    objective: str
    started_at: str
    completed_at: str
    status: str
    phase_results: dict[int, list[TaskRecord]]
    shared_results: dict[str, Any]
    messages: list[dict[str, Any]]


@dataclass(slots=True)
class AgentOrchestrator:
    """Coordinates multi-agent collaboration with phased parallel execution."""

    agent_kernel: AgentKernel
    task_scheduler: TaskScheduler = field(default_factory=TaskScheduler)
    communication_bus: AgentCommunicationBus = field(default_factory=AgentCommunicationBus)
    shared_memory: SharedMemory = field(default_factory=SharedMemory)
    max_workers: int = 4

    def run_collaboration(
        self,
        objective: str,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> CollaborationResult:
        collaboration_id = str(uuid4())
        started_at = datetime.now(timezone.utc).isoformat()
        schedule = self.task_scheduler.build_schedule(objective)
        self.shared_memory.store_context(collaboration_id, "objective", objective)

        phase_results: dict[int, list[TaskRecord]] = {}
        for phase in sorted({item.phase for item in schedule}):
            phase_tasks = [item for item in schedule if item.phase == phase]
            results = self._run_phase(
                collaboration_id,
                phase_tasks,
                user_id=user_id,
                session_id=session_id,
            )
            phase_results[phase] = results

        completed_at = datetime.now(timezone.utc).isoformat()
        return CollaborationResult(
            collaboration_id=collaboration_id,
            objective=objective,
            started_at=started_at,
            completed_at=completed_at,
            status="completed",
            phase_results=phase_results,
            shared_results=self.shared_memory.get_results(collaboration_id),
            messages=self.communication_bus.get_messages(collaboration_id),
        )

    def _run_phase(
        self,
        collaboration_id: str,
        tasks: list[ScheduledAgentTask],
        *,
        user_id: str | None,
        session_id: str | None,
    ) -> list[TaskRecord]:
        def execute(item: ScheduledAgentTask) -> TaskRecord:
            self.communication_bus.publish(
                collaboration_id,
                sender="CoordinatorAgent",
                recipient=item.agent_name,
                message_type="task_assigned",
                payload={"description": item.task_description, "capability": item.capability},
            )

            capability = CAPABILITY_MAP.get(item.capability, AgentCapability.RESEARCH)
            record = self.agent_kernel.receive_user_task(
                description=item.task_description,
                capability=capability,
                user_id=user_id,
                session_id=session_id,
                metadata={"collaboration_agent": item.agent_name, "collaboration_id": collaboration_id},
            )

            self.shared_memory.store_result(
                collaboration_id,
                item.agent_name,
                {
                    "task_id": record.task_id,
                    "status": record.status.value,
                    "output": record.result.output if record.result else "",
                },
            )
            self.communication_bus.publish(
                collaboration_id,
                sender=item.agent_name,
                recipient="CoordinatorAgent",
                message_type="task_completed",
                payload={"task_id": record.task_id, "status": record.status.value},
            )
            return record

        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(tasks) or 1)) as executor:
            return list(executor.map(execute, tasks))
