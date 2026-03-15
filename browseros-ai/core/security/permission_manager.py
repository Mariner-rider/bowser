"""Permission boundary manager."""


class PermissionManager:
    def __init__(self) -> None:
        self._grants: dict[str, set[str]] = {}

    def grant(self, agent_name: str, permission: str) -> None:
        self._grants.setdefault(agent_name, set()).add(permission)

    def has(self, agent_name: str, permission: str) -> bool:
        return permission in self._grants.get(agent_name, set())
