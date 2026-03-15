"""AI-powered privacy and security guardian for browser sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SecurityScanResult:
    risk_level: str
    warnings: list[str]
    indicators: dict[str, Any]


@dataclass(slots=True)
class PrivacySecurityGuardian:
    """Detects phishing, malicious scripts, suspicious downloads, cookies, and extension risk."""

    blocked_domains: set[str] = field(default_factory=set)

    def scan_page(
        self,
        *,
        url: str,
        page_title: str,
        script_sources: list[str],
        login_form_present: bool,
    ) -> SecurityScanResult:
        warnings: list[str] = []
        indicators: dict[str, Any] = {
            "url": url,
            "page_title": page_title,
            "third_party_scripts": len(script_sources),
            "login_form_present": login_form_present,
        }

        host = _host_from_url(url)
        if host in self.blocked_domains:
            warnings.append("Known malicious domain")

        if login_form_present and any(k in page_title.lower() for k in ["verify account", "urgent", "suspended"]):
            warnings.append("Possible fake login page pattern")

        if any("xn--" in src or src.endswith(".ru") for src in script_sources):
            warnings.append("Suspicious script source detected")

        if "paypa1" in host or "micros0ft" in host:
            warnings.append("Potential domain impersonation / mismatch")

        risk = "high" if len(warnings) >= 2 else "medium" if warnings else "low"
        return SecurityScanResult(risk_level=risk, warnings=warnings, indicators=indicators)

    def monitor_download(self, filename: str, source_url: str) -> SecurityScanResult:
        warnings: list[str] = []
        lower_name = filename.lower()

        if lower_name.endswith((".exe", ".scr", ".bat")):
            warnings.append("Executable download requires caution")
        if "free-crypto" in source_url or "keygen" in source_url:
            warnings.append("Suspicious download source pattern")

        risk = "high" if len(warnings) >= 2 else "medium" if warnings else "low"
        return SecurityScanResult(risk_level=risk, warnings=warnings, indicators={"filename": filename, "source_url": source_url})

    def monitor_tracking_cookies(self, cookies: list[dict[str, Any]]) -> SecurityScanResult:
        third_party = [c for c in cookies if c.get("third_party")]
        warnings: list[str] = []
        if len(third_party) > 10:
            warnings.append("Excessive third-party tracking cookies")

        risk = "medium" if warnings else "low"
        return SecurityScanResult(risk_level=risk, warnings=warnings, indicators={"cookies_total": len(cookies), "third_party": len(third_party)})

    def scan_extensions(self, extensions: list[dict[str, Any]]) -> SecurityScanResult:
        risky = [e for e in extensions if e.get("permissions") and "<all_urls>" in e.get("permissions", [])]
        warnings = [f"Extension '{e.get('name', 'unknown')}' has broad <all_urls> permission" for e in risky]

        risk = "high" if len(risky) >= 2 else "medium" if risky else "low"
        return SecurityScanResult(risk_level=risk, warnings=warnings, indicators={"extension_count": len(extensions), "risky": len(risky)})

    def warning_banner(self, scan: SecurityScanResult) -> str | None:
        if scan.risk_level == "high":
            return "⚠ Possible phishing attempt"
        if scan.risk_level == "medium":
            return "⚠ Suspicious activity detected"
        return None


def _host_from_url(url: str) -> str:
    no_proto = url.replace("https://", "").replace("http://", "")
    return no_proto.split("/")[0].lower()
