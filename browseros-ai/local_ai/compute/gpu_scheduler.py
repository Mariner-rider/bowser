"""GPU scheduler for local inference workloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .resource_monitor import ResourceMonitor


@dataclass(slots=True)
class GPUScheduler:
    """Queues and prioritizes local AI workloads against GPU resources."""

    monitor: ResourceMonitor = field(default_factory=ResourceMonitor)
    queue: list[dict[str, Any]] = field(default_factory=list)

    def enqueue(self, workload: dict[str, Any]) -> None:
        self.queue.append(workload)

    def allocate_next(self) -> dict[str, Any] | None:
        if not self.queue:
            return None

        snapshot = self.monitor.snapshot()
        if not snapshot.get("gpu_available"):
            return None

        # Prioritize lower estimated memory first in this scaffold.
        self.queue.sort(key=lambda w: float(w.get("estimated_gpu_gb", 2.0)))
        return self.queue.pop(0)

    def status(self) -> dict[str, Any]:
        return {
            "queued": len(self.queue),
            "resources": self.monitor.snapshot(),
        }
