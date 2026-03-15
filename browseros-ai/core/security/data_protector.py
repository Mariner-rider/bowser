"""Data protection utilities for masking and reversible secure payload sealing.

Goal: minimize accidental leakage in logs while allowing explicit decrypt/unseal paths
when authorized.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
import hashlib
import hmac
import json
import secrets
from typing import Any

_SENSITIVE_KEYS = {
    "password",
    "passphrase",
    "secret",
    "token",
    "api_key",
    "private_key",
    "seed_phrase",
    "wallet_secret",
    "signature",
    "credential",
    "auth",
}


@dataclass(slots=True)
class SecureDataProtector:
    """Provides reversible seal/unseal and non-reversible masking helpers."""

    master_key: str
    iterations: int = 120_000
    _salt_size: int = 16
    _nonce_size: int = 16

    def seal(self, payload: dict[str, Any]) -> str:
        """Encrypt-like seal using derived keystream + integrity MAC.

        This is a clean-room implementation for local protection needs.
        """
        serialized = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        salt = secrets.token_bytes(self._salt_size)
        nonce = secrets.token_bytes(self._nonce_size)
        key = self._derive_key(salt)
        stream = self._keystream(key, nonce, len(serialized))
        cipher = bytes(a ^ b for a, b in zip(serialized, stream))
        mac = hmac.new(key, nonce + cipher, hashlib.sha256).digest()
        packed = salt + nonce + mac + cipher
        return base64.urlsafe_b64encode(packed).decode("utf-8")

    def unseal(self, token: str) -> dict[str, Any]:
        raw = base64.urlsafe_b64decode(token.encode("utf-8"))
        header_len = self._salt_size + self._nonce_size + 32
        if len(raw) <= header_len:
            raise ValueError("Invalid sealed payload")

        salt = raw[: self._salt_size]
        nonce = raw[self._salt_size : self._salt_size + self._nonce_size]
        mac = raw[self._salt_size + self._nonce_size : header_len]
        cipher = raw[header_len:]

        key = self._derive_key(salt)
        expected = hmac.new(key, nonce + cipher, hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected):
            raise ValueError("Integrity check failed")

        stream = self._keystream(key, nonce, len(cipher))
        plain = bytes(a ^ b for a, b in zip(cipher, stream))
        return json.loads(plain.decode("utf-8"))

    def mask_text(self, value: str, *, keep: int = 2) -> str:
        if not value:
            return value
        if len(value) <= keep * 2:
            return "*" * len(value)
        return f"{value[:keep]}{'*' * (len(value) - keep * 2)}{value[-keep:]}"

    def mask_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        masked: dict[str, Any] = {}
        for key, value in payload.items():
            lowered = key.lower()
            if lowered in _SENSITIVE_KEYS and isinstance(value, str):
                masked[key] = self.mask_text(value)
            elif isinstance(value, dict):
                masked[key] = self.mask_payload(value)
            elif isinstance(value, list):
                masked[key] = [self.mask_payload(v) if isinstance(v, dict) else v for v in value]
            else:
                masked[key] = value
        return masked

    def _derive_key(self, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", self.master_key.encode("utf-8"), salt, self.iterations, dklen=32)

    def _keystream(self, key: bytes, nonce: bytes, size: int) -> bytes:
        out = bytearray()
        counter = 0
        while len(out) < size:
            block = hmac.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest()
            out.extend(block)
            counter += 1
        return bytes(out[:size])


def default_protector() -> SecureDataProtector:
    return SecureDataProtector(master_key="local-dev-key-change-in-prod")
