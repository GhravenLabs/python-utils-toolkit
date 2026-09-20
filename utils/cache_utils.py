"""In-memory TTL cache and memoize decorator — useful for rate-limited APIs."""

from __future__ import annotations
import functools
import math
import time
from threading import Lock
from typing import Any, Callable


class TTLCache:
    """Thread-safe in-memory cache with time-to-live expiry.

    Useful for caching API responses (price data, market info) without
    hitting rate limits on every call.

    Args:
        ttl: Finite time-to-live in seconds (default 60).
        maxsize: Positive integer limit on entries (earliest expiry evicted first).

    Example:
        >>> cache = TTLCache(ttl=30)
        >>> cache.set("BTC_price", 87500.0)
        >>> cache.get("BTC_price")
        87500.0
    """

    def __init__(self, ttl: float = 60.0, maxsize: int = 1000) -> None:
        if isinstance(maxsize, bool) or not isinstance(maxsize, int) or maxsize < 1:
            raise ValueError("maxsize must be a positive integer")
        if not math.isfinite(ttl):
            raise ValueError("ttl must be finite")
        self._ttl = ttl
        self._maxsize = maxsize
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = Lock()

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            value, expires_at = entry
            if time.monotonic() >= expires_at:
                del self._store[key]
                return default
            return value

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Store a value; None uses the default TTL and zero expires immediately."""
        effective_ttl = self._ttl if ttl is None else ttl
        if not math.isfinite(effective_ttl):
            raise ValueError("ttl must be finite")
        with self._lock:
            if key not in self._store and len(self._store) >= self._maxsize:
                # Evict oldest entry
                oldest = min(self._store, key=lambda k: self._store[k][1])
                del self._store[oldest]
            expires_at = time.monotonic() + effective_ttl
            self._store[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def __contains__(self, key: str) -> bool:
        missing = object()
        return self.get(key, missing) is not missing


def memoize(ttl: float = 60.0):
    """Decorator that caches function results with TTL.

    >>> @memoize(ttl=30)
    ... def get_ticker_info(symbol: str) -> dict:
    ...     return api.get_ticker(symbol)  # only called once per 30s
    """
    def decorator(func: Callable) -> Callable:
        cache = TTLCache(ttl=ttl)
        missing = object()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            result = cache.get(key, missing)
            if result is missing:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result
        return wrapper
    return decorator
