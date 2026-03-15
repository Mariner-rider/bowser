"""Browser session adapter backed by the local BrowserOSRuntime."""

from __future__ import annotations

from dataclasses import dataclass

from .browseros_runtime import BrowserOSRuntime


@dataclass(slots=True)
class RuntimeBrowserSession:
    runtime: BrowserOSRuntime

    def navigate(self, url: str) -> None:
        self.runtime.navigate(url)

    def click(self, selector: str) -> None:
        self.runtime.click(selector)

    def type_text(self, selector: str, text: str) -> None:
        self.runtime.type_text(selector, text)

    def scroll(self, amount: int) -> None:
        self.runtime.scroll(amount)
