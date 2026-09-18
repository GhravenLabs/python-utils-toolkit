"""Timing utilities — decorator and context manager.

Usage
-----
>>> @timer
... def slow_function():
...     time.sleep(1)

>>> with Timer("database query") as t:
...     run_query()
... print(f"Query took {t.elapsed:.3f}s")
"""

from __future__ import annotations

import functools
import inspect
import logging
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


def timer(func: F) -> F:
    """Decorator that logs how long a function takes to run.

    Example
    -------
    >>> @timer
    ... def analyze_market(symbol: str) -> dict:
    ...     ...
    """

    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                logger.info("%s completed in %.4fs", func.__name__, elapsed)
        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.info("%s completed in %.4fs", func.__name__, elapsed)

    return wrapper  # type: ignore[return-value]


class Timer:
    """Context manager for timing code blocks.

    Attributes
    ----------
    elapsed:
        Seconds elapsed between ``__enter__`` and ``__exit__``.
        Available after the ``with`` block completes.

    Example
    -------
    >>> with Timer("signal generation") as t:
    ...     generate_signals()
    ... print(f"Took {t.elapsed:.2f}s")
    """

    def __init__(self, name: str = "", log: bool = True) -> None:
        self.name = name
        self._log = log
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_) -> None:
        self.elapsed = time.perf_counter() - self._start
        if self._log and self.name:
            logger.info("[timer] %s took %.4fs", self.name, self.elapsed)
