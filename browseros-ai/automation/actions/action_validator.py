"""Validation layer for automation actions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ActionValidator:
    """Validates action inputs before execution."""

    def validate_url(self, url: str) -> None:
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

    def validate_selector(self, selector: str) -> None:
        if not selector.strip():
            raise ValueError("Selector cannot be empty")

    def validate_text(self, text: str) -> None:
        if text is None:
            raise ValueError("Text input cannot be None")

    def validate_scroll(self, amount: int) -> None:
        if amount == 0:
            raise ValueError("Scroll amount cannot be zero")
