"""Retry decorator with exponential backoff and optional jitter.

Usage
-----
>>> @retry(max_attempts=3, base_delay=1.0, exceptions=(ConnectionError,))
... def fetch():
...     ...
"""

from __future__ import annotations

import functools
import logging
import math
import random
import time
from typing import Callable, Tuple, Type, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


def _validate_retry(max_attempts: int, base_delay: float, backoff: float) -> None:
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if not math.isfinite(base_delay) or base_delay < 0:
        raise ValueError("base_delay must be finite and nonnegative")
    if not math.isfinite(backoff) or backoff < 0:
        raise ValueError("backoff must be finite and nonnegative")


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Retry a function on failure with exponential backoff.

    Parameters
    ----------
    max_attempts:
        Total number of attempts (including the first call).
    base_delay:
        Initial wait time in seconds after the first failure.
    max_delay:
        Upper bound on wait time regardless of backoff.
    backoff:
        Multiplier applied to the delay after each failure.
    jitter:
        Add ±25 % random noise to prevent thundering herd.
    exceptions:
        Tuple of exception types that trigger a retry.
        All other exceptions propagate immediately.

    Returns
    -------
    Callable
        The decorated function.

    Example
    -------
    >>> @retry(max_attempts=5, base_delay=0.5, exceptions=(TimeoutError,))
    ... def call_api(url: str) -> dict:
    ...     return requests.get(url).json()
    """

    _validate_retry(max_attempts, base_delay, backoff)
    if not math.isfinite(max_delay) or max_delay < 0:
        raise ValueError("max_delay must be finite and nonnegative")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exc: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == max_attempts:
                        logger.error(
                            "%s failed after %d attempts: %s",
                            func.__name__,
                            max_attempts,
                            exc,
                        )
                        raise

                    wait = min(delay, max_delay)
                    if jitter:
                        wait *= random.uniform(0.75, 1.25)
                    wait = min(wait, max_delay)
                    logger.warning(
                        "%s attempt %d/%d failed (%s). Retrying in %.2fs…",
                        func.__name__,
                        attempt,
                        max_attempts,
                        exc,
                        wait,
                    )
                    time.sleep(wait)
                    delay *= backoff

            raise last_exc  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator
