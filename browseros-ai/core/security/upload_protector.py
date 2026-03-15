"""Upload security utilities for masking and reversible protection of upload payloads."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

from .data_protector import SecureDataProtector, default_protector


@dataclass(slots=True)
class UploadProtector:
    """Protects upload metadata/content using the core data protector."""

    data_protector: SecureDataProtector

    def seal_upload(self, *, filename: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        payload = {
            "filename": filename,
            "content_b64": base64.b64encode(content).decode("utf-8"),
            "content_type": content_type,
            "size": len(content),
        }
        return self.data_protector.seal(payload)

    def unseal_upload(self, sealed_token: str) -> dict[str, Any]:
        payload = self.data_protector.unseal(sealed_token)
        return {
            "filename": str(payload["filename"]),
            "content": base64.b64decode(str(payload["content_b64"]).encode("utf-8")),
            "content_type": str(payload.get("content_type", "application/octet-stream")),
            "size": int(payload.get("size", 0)),
        }

    def mask_upload_metadata(self, *, filename: str, content_type: str, size: int) -> dict[str, Any]:
        masked = self.data_protector.mask_payload(
            {
                "filename": filename,
                "content_type": content_type,
                "size": size,
            }
        )
        if isinstance(masked.get("filename"), str):
            masked["filename"] = self.data_protector.mask_text(masked["filename"], keep=1)
        return masked


def default_upload_protector() -> UploadProtector:
    return UploadProtector(data_protector=default_protector())
