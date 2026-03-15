"""Action execution primitives for autonomous browser workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol

from .action_validator import ActionValidator


class BrowserSession(Protocol):
    """Abstraction over browser automation runtime (Playwright/WebDriver/etc.)."""

    def navigate(self, url: str) -> None:
        ...

    def click(self, selector: str) -> None:
        ...

    def type_text(self, selector: str, text: str) -> None:
        ...

    def scroll(self, amount: int) -> None:
        ...


@dataclass(slots=True)
class ActionExecutor:
    """Executes validated actions and records a full action log."""

    session: BrowserSession
    validator: ActionValidator = field(default_factory=ActionValidator)
    action_log: list[dict[str, Any]] = field(default_factory=list)

    def click_element(self, selector: str) -> None:
        self.validator.validate_selector(selector)
        self.session.click(selector)
        self._log_action("click_element", {"selector": selector})

    def type_text(self, selector: str, text: str) -> None:
        self.validator.validate_selector(selector)
        self.validator.validate_text(text)
        self.session.type_text(selector, text)
        self._log_action("type_text", {"selector": selector, "text_length": len(text)})

    def scroll_page(self, amount: int) -> None:
        self.validator.validate_scroll(amount)
        self.session.scroll(amount)
        self._log_action("scroll_page", {"amount": amount})

    def navigate_url(self, url: str) -> None:
        self.validator.validate_url(url)
        self.session.navigate(url)
        self._log_action("navigate_url", {"url": url})

    def get_action_log(self) -> list[dict[str, Any]]:
        return list(self.action_log)

    def _log_action(self, action: str, payload: dict[str, Any]) -> None:
        self.action_log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "payload": payload,
            }
        )
