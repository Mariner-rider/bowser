"""Base agent contracts and shared domain models for BrowserOS AI agents."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class AgentCapability(str, Enum):
    """Capabilities used by the kernel for routing and policy checks."""

    RESEARCH = "research"
    AUTOMATION = "automation"
    CODING = "coding"
    SHOPPING = "shopping"
    SECURITY = "security"
    PRODUCTIVITY = "productivity"


class TaskStatus(str, Enum):
    """Task lifecycle status managed by the AgentKernel."""

    RECEIVED = "received"
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class TaskContext:
    """Context metadata propagated across modules."""

    task_id: str
    user_id: str | None = None
    session_id: str | None = None
    trace_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TaskRequest:
    """Incoming task envelope for an agent."""

    description: str
    capability: AgentCapability
    constraints: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TaskPlan:
    """Planner output consumed by execute_task."""

    steps: list[str]
    rationale: str


@dataclass(slots=True)
class TaskResult:
    """Result envelope produced by an agent."""

    success: bool
    output: str
    artifacts: dict[str, Any] = field(default_factory=dict)


class LLMRouter(Protocol):
    """LLM integration contract."""

    def generate(self, task: str, prompt: str, context: TaskContext) -> str:
        """Return model output for a prompt."""


class MemoryEngine(Protocol):
    """Memory integration contract."""

    def remember(self, namespace: str, key: str, value: Any) -> None:
        """Persist a value."""

    def recall(self, namespace: str, key: str) -> Any:
        """Load a previously persisted value."""


class AutomationEngine(Protocol):
    """Automation integration contract."""

    def run(self, objective: str, context: TaskContext) -> dict[str, Any]:
        """Execute an automation objective and return details."""


class AgentBase(ABC):
    """Abstract base class that all specialized agents extend."""

    def __init__(
        self,
        name: str,
        capability: AgentCapability,
        llm_router: LLMRouter,
        memory_engine: MemoryEngine,
        automation_engine: AutomationEngine,
    ) -> None:
        self.name = name
        self.capability = capability
        self.llm_router = llm_router
        self.memory_engine = memory_engine
        self.automation_engine = automation_engine

    @abstractmethod
    def plan_task(self, task: TaskRequest, context: TaskContext) -> TaskPlan:
        """Create a structured plan for the incoming task."""

    @abstractmethod
    def call_tools(self, plan: TaskPlan, context: TaskContext) -> dict[str, Any]:
        """Invoke tools/services needed to execute the task."""

    @abstractmethod
    def execute_task(self, task: TaskRequest, context: TaskContext) -> TaskResult:
        """Run a full task execution flow for this agent."""
