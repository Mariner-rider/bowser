"""Interprets workflow step descriptions into executable action plans."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .element_locator import ElementLocator


@dataclass(slots=True)
class PageInterpreter:
    """Normalizes workflow steps and resolves element selectors."""

    locator: ElementLocator

    def interpret_step(self, step: dict[str, Any]) -> dict[str, Any]:
        action = step["action"]
        normalized = {"action": action, **step}

        if action in {"click", "type"} and "target" in step:
            normalized["selector"] = self.locator.locate(step["target"])

        return normalized
