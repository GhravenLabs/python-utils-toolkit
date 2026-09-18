"""Dictionary manipulation utilities."""

from __future__ import annotations
from typing import Any


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base* (non-destructive).

    >>> deep_merge({"a": {"x": 1}}, {"a": {"y": 2}})
    {'a': {'x': 1, 'y': 2}}
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def safe_get(d: dict, *keys: str, default: Any = None) -> Any:
    """Safely navigate nested dict with fallback.

    >>> safe_get({"a": {"b": 42}}, "a", "b")
    42
    >>> safe_get({}, "a", "b", default=0)
    0
    """
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def flatten_dict(d: dict, separator: str = ".", prefix: str = "") -> dict:
    """Flatten nested dict into a single level with dotted keys.

    >>> flatten_dict({"a": {"b": 1, "c": 2}})
    {'a.b': 1, 'a.c': 2}
    """
    items = {}
    for key, value in d.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, separator, new_key))
        else:
            items[new_key] = value
    return items


def pick(d: dict, *keys: str) -> dict:
    """Return a new dict with only the specified keys.

    >>> pick({"a": 1, "b": 2, "c": 3}, "a", "c")
    {'a': 1, 'c': 3}
    """
    return {k: d[k] for k in keys if k in d}


def omit(d: dict, *keys: str) -> dict:
    """Return a new dict without the specified keys.

    >>> omit({"a": 1, "b": 2, "c": 3}, "b")
    {'a': 1, 'c': 3}
    """
    return {k: v for k, v in d.items() if k not in keys}
