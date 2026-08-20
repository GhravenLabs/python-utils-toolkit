"""Hashing and HMAC utilities for signed API requests."""

from __future__ import annotations
import hashlib
import hmac
import secrets
import time


def hmac_sha256(secret: str, message: str) -> str:
    """Generate an HMAC-SHA256 signature.

    Args:
        secret: Your API secret key.
        message: The query string or payload to sign.

    Returns:
        Hex-encoded HMAC-SHA256 signature.

    Example:
        >>> sig = hmac_sha256("my_secret", "client=ACME42&action=export")
    """
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def sha256(data: str | bytes) -> str:
    """Return SHA-256 hash of data as hex string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def md5(data: str | bytes) -> str:
    """Return MD5 hash of data as hex string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.md5(data).hexdigest()  # noqa: S324


def generate_nonce(length: int = 32) -> str:
    """Generate a cryptographically secure random nonce."""
    return secrets.token_hex(length // 2)


def timestamp_nonce() -> str:
    """Generate a timestamp-based nonce for API requests."""
    return str(int(time.time() * 1000))
