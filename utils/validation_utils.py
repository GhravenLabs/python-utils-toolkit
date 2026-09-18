"""Input validation helpers — guard clauses and type checkers."""

from __future__ import annotations
import re
from typing import Any


def is_positive_number(value: Any) -> bool:
    """Check if value is a positive int or float."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def is_valid_symbol(symbol: str) -> bool:
    """Check if a compact uppercase identifier uses a safe symbol format.

    >>> is_valid_symbol("CLIENT42")
    True
    >>> is_valid_symbol("TEAM/API")
    True
    >>> is_valid_symbol("")
    False
    """
    if not symbol or not isinstance(symbol, str):
        return False
    return bool(re.fullmatch(r"[A-Z0-9]{2,20}(/[A-Z0-9]{2,10})?", symbol.upper()))


def is_valid_email(email: str) -> bool:
    """Basic email format check.

    >>> is_valid_email("user@example.com")
    True
    """
    return isinstance(email, str) and bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def require(condition: bool, message: str) -> None:
    """Raise ValueError with *message* if *condition* is False.

    >>> require(price > 0, "price must be positive")
    """
    if not condition:
        raise ValueError(message)


def require_keys(d: dict, *keys: str) -> None:
    """Raise KeyError if any required keys are missing from dict.

    >>> require_keys(config, "api_key", "secret", "symbol")
    """
    missing = [k for k in keys if k not in d]
    if missing:
        raise KeyError(f"Missing required keys: {missing}")


def is_within_range(value: float, low: float, high: float, inclusive: bool = True) -> bool:
    """Check if value falls within [low, high] range."""
    if inclusive:
        return low <= value <= high
    return low < value < high
