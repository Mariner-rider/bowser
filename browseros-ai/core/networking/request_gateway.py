"""Network request mediation for AI modules."""


def allow_request(url: str) -> bool:
    """Return whether url is allowed by policy."""
    blocked_prefixes = ("file://", "chrome://")
    return not url.startswith(blocked_prefixes)
