"""Element location strategy resolver."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ElementLocator:
    """Converts semantic targets into CSS selectors."""

    def locate(self, target: str) -> str:
        target = target.strip()
        if target.startswith(("#", ".", "[")):
            return target
        return f"[data-testid='{target}']"
