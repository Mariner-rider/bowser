"""Cross-module API protocol definitions for BrowserOS AI.

These protocols formalize the boundaries described in docs/architecture.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class RequestContext:
    request_id: str
    trace_id: str
    user_id: str | None = None
    session_id: str | None = None
    risk_level: str = "low"
    auth_scopes: list[str] = field(default_factory=list)


class AgentKernelAPI(Protocol):
    def submit_task(self, task: dict[str, Any], context: RequestContext) -> str:
        """Submit a task and return task_id."""

    def get_task_status(self, task_id: str, context: RequestContext) -> dict[str, Any]:
        """Return lifecycle information for an existing task."""

    def cancel_task(self, task_id: str, context: RequestContext) -> bool:
        """Cancel a running or queued task."""


class LLMRouterAPI(Protocol):
    def generate(self, prompt: str, context: RequestContext) -> str:
        """Generate model output for a prompt."""

    def stream(self, prompt: str, context: RequestContext) -> Any:
        """Stream model output chunks."""

    def embed(self, text: str, context: RequestContext) -> list[float]:
        """Return embedding vector for text."""


class MemoryEngineAPI(Protocol):
    def store_memory(self, data: dict[str, Any], context: RequestContext) -> str:
        """Store memory record and return memory_id/version."""

    def search_memory(self, query: str, context: RequestContext) -> list[dict[str, Any]]:
        """Run semantic or structured memory search."""

    def retrieve_context(self, context: RequestContext) -> dict[str, Any]:
        """Fetch contextual bundle for current request."""


class AutomationEngineAPI(Protocol):
    def execute_action(self, action: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Execute a single validated browser action."""

    def run_workflow(self, workflow: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Execute a workflow and return run metadata."""


class LearningEngineAPI(Protocol):
    def collect_feedback(self, event: dict[str, Any], context: RequestContext) -> None:
        """Ingest user/system feedback signal."""

    def train_policy(self, batch: list[dict[str, Any]], context: RequestContext) -> dict[str, Any]:
        """Train or update policy from interactions."""

    def update_preferences(self, user_id: str, context: RequestContext) -> dict[str, Any]:
        """Update preference model for user."""


class LocalAIEngineAPI(Protocol):
    def load_model(self, model_id: str, context: RequestContext) -> bool:
        """Ensure local model is present and loaded."""

    def run_inference(self, request: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Run local inference request."""

    def schedule_workload(self, workload: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Schedule compute workload on local resources."""


class DashboardAPI(Protocol):
    def publish_event(self, event: dict[str, Any], context: RequestContext) -> None:
        """Publish telemetry event."""

    def get_system_snapshot(self, context: RequestContext) -> dict[str, Any]:
        """Return current system health/status summary."""

    def get_task_timeline(self, task_id: str, context: RequestContext) -> list[dict[str, Any]]:
        """Return ordered timeline events for task."""


class Web3LayerAPI(Protocol):
    def connect_wallet(self, request: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Connect wallet provider and return account metadata."""

    def verify_identity(self, address: str, signature: str, context: RequestContext) -> bool:
        """Verify wallet signature for identity/auth."""

    def authorize_feature(self, token: str, capability: str, context: RequestContext) -> bool:
        """Authorize capability via token policy."""


class CapacitorRuntimeAPI(Protocol):
    def initialize_mobile_runtime(self, context: RequestContext) -> dict[str, Any]:
        """Initialize runtime inside mobile shell."""

    def sync_web_assets(self, context: RequestContext) -> dict[str, Any]:
        """Sync built web assets with native projects."""

    def invoke_native_capability(self, name: str, payload: dict[str, Any], context: RequestContext) -> dict[str, Any]:
        """Invoke named native capability from web runtime."""
