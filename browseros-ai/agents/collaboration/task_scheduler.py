"""Task scheduler for parallel multi-agent collaboration plans."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ScheduledAgentTask:
    """Represents an execution unit assigned to a specific agent capability."""

    agent_name: str
    capability: str
    task_description: str
    phase: int


@dataclass(slots=True)
class TaskScheduler:
    """Builds phased schedules for collaborative workflows."""

    def build_schedule(self, objective: str) -> list[ScheduledAgentTask]:
        objective_lower = objective.lower()

        # Example collaborative template for report-style objectives.
        if "report" in objective_lower:
            return [
                ScheduledAgentTask(
                    agent_name="ResearchAgent",
                    capability="research",
                    task_description=f"Collect sources and findings for: {objective}",
                    phase=1,
                ),
                ScheduledAgentTask(
                    agent_name="DataAgent",
                    capability="research",
                    task_description=f"Extract structured statistics for: {objective}",
                    phase=1,
                ),
                ScheduledAgentTask(
                    agent_name="FinanceAgent",
                    capability="research",
                    task_description=f"Analyze funding and financial trends for: {objective}",
                    phase=1,
                ),
                ScheduledAgentTask(
                    agent_name="WriterAgent",
                    capability="research",
                    task_description=f"Synthesize final report for: {objective}",
                    phase=2,
                ),
            ]

        # Generic fallback collaboration template.
        return [
            ScheduledAgentTask(
                agent_name="ResearchAgent",
                capability="research",
                task_description=f"Research objective context: {objective}",
                phase=1,
            ),
            ScheduledAgentTask(
                agent_name="WriterAgent",
                capability="research",
                task_description=f"Produce concise deliverable for: {objective}",
                phase=2,
            ),
        ]
