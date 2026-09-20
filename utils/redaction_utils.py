"""Small privacy helpers for logs, prompts, and support exports."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
TOKEN_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9_]{12,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)

DEFAULT_SECRET_KEYS = {
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "password",
    "secret",
    "token",
}


def mask_email(value: str) -> str:
    """Mask an email while keeping enough shape for debugging."""
    local, _, domain = value.partition("@")
    if not local or not domain:
        return "[REDACTED_EMAIL]"
    head = local[:1]
    tail = local[-1:] if len(local) > 1 else ""
    return f"{head}***{tail}@{domain}"


def redact_text(text: str, replacement: str = "[REDACTED]") -> str:
    """Redact common personal data and API tokens from a string."""
    redacted = TOKEN_RE.sub(lambda match: replacement, text)
    redacted = EMAIL_RE.sub(lambda match: mask_email(match.group(0)), redacted)
    return PHONE_RE.sub("[REDACTED_PHONE]", redacted)


def redact_mapping(
    data: Mapping[str, Any],
    secret_keys: set[str] | None = None,
    replacement: str = "[REDACTED]",
) -> dict[str, Any]:
    """Return a copy of a mapping with sensitive keys and string values redacted."""
    blocked = {key.lower() for key in (DEFAULT_SECRET_KEYS if secret_keys is None else secret_keys)}
    def clean_value(value):
        if isinstance(value, str):
            return redact_text(value, replacement=replacement)
        if isinstance(value, Mapping):
            return redact_mapping(value, secret_keys=blocked, replacement=replacement)
        if isinstance(value, (list, tuple)):
            return type(value)(clean_value(item) for item in value)
        return value

    clean: dict[str, Any] = {}
    for key, value in data.items():
        key_lower = str(key).lower()
        if key_lower in blocked or any(part in key_lower for part in blocked):
            clean[key] = replacement
        else:
            clean[key] = clean_value(value)
    return clean
