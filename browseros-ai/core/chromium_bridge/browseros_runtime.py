"""Clean-room BrowserOS-compatible runtime implementation.

This module provides an embeddable browser runtime abstraction implemented from
scratch so the project can run end-to-end without cloning external repositories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class BrowserTab:
    tab_id: str
    url: str = "about:blank"
    dom_state: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BrowserOSRuntime:
    """Minimal local runtime with deterministic action log."""

    tabs: dict[str, BrowserTab] = field(default_factory=dict)
    active_tab_id: str = "tab-1"
    action_log: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.active_tab_id not in self.tabs:
            self.tabs[self.active_tab_id] = BrowserTab(tab_id=self.active_tab_id)

    def navigate(self, url: str) -> None:
        self._active_tab().url = url
        self._log("navigate", {"url": url})

    def click(self, selector: str) -> None:
        self._log("click", {"selector": selector})

    def type_text(self, selector: str, text: str) -> None:
        self._active_tab().dom_state[selector] = text
        self._log("type", {"selector": selector, "text_length": len(text)})

    def scroll(self, amount: int) -> None:
        self._log("scroll", {"amount": amount})

    def snapshot(self) -> dict[str, Any]:
        tab = self._active_tab()
        return {
            "active_tab_id": tab.tab_id,
            "url": tab.url,
            "dom_state": dict(tab.dom_state),
            "actions": list(self.action_log),
        }

    def _active_tab(self) -> BrowserTab:
        return self.tabs[self.active_tab_id]

    def _log(self, action: str, payload: dict[str, Any]) -> None:
        self.action_log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "payload": payload,
            }
        )
