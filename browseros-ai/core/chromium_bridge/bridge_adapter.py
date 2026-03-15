"""Bridge adapter contracts for safe BrowserOS integration."""

from dataclasses import dataclass


@dataclass(slots=True)
class BridgeEvent:
    name: str
    payload: dict[str, object]


class ChromiumBridgeAdapter:
    """Minimal bridge scaffold used by ai modules."""

    def emit(self, event: BridgeEvent) -> None:
        """Emit extension event to BrowserOS runtime."""

    def can_execute_capability(self, capability: str) -> bool:
        """Policy gate for capability execution."""
        return True
