"""Resource monitor for CPU/GPU/memory signals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ResourceMonitor:
    """Collects lightweight resource snapshots for local scheduling."""

    def snapshot(self) -> dict[str, Any]:
        # Stubbed values for portable scaffold runtime.
        return {
            "cpu_percent": 35.0,
            "ram_percent": 48.0,
            "gpu_available": True,
            "gpu_memory_free_gb": 8.0,
            "power_mode": "balanced",
        }
