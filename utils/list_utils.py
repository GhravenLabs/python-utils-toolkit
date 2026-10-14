"""List manipulation utilities."""

from __future__ import annotations
from typing import Any, Generator, Iterable, TypeVar

T = TypeVar("T")


def chunk(lst: list[T], size: int) -> Generator[list[T], None, None]:
    """Split list into chunks of *size*.

    >>> list(chunk([1,2,3,4,5], 2))
    [[1, 2], [3, 4], [5]]
    """
    if isinstance(size, bool) or not isinstance(size, int) or size < 1:
        raise ValueError("size must be a positive integer")
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def flatten(nested: Iterable[Any], depth: int = 1) -> list[Any]:
    """Flatten a nested list up to *depth* levels.

    >>> flatten([[1, 2], [3, [4, 5]]])
    [1, 2, 3, [4, 5]]
    """
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    result = []
    for item in nested:
        if isinstance(item, (list, tuple)) and depth > 0:
            result.extend(flatten(item, depth - 1))
        else:
            result.append(item)
    return result


def deduplicate(lst: list[T], preserve_order: bool = True) -> list[T]:
    """Remove equal duplicates, including unhashable lists and dictionaries.

    >>> deduplicate([1, 2, 1, 3, 2])
    [1, 2, 3]
    """
    if preserve_order:
        result: list[T] = []
        seen_hashable: set = set()
        for item in lst:
            try:
                if item in seen_hashable:
                    continue
                seen_hashable.add(item)
            except TypeError:
                if any(item == previous for previous in result):
                    continue
            result.append(item)
        return result
    return list(set(lst))


def first(lst: list[T], default: T | None = None) -> T | None:
    """Return first element or *default* if empty."""
    return lst[0] if lst else default


def last(lst: list[T], default: T | None = None) -> T | None:
    """Return last element or *default* if empty."""
    return lst[-1] if lst else default


def batch_by(items: list[T], key) -> dict[Any, list[T]]:
    """Group list items by a key function.

    >>> batch_by([1,2,3,4], lambda x: x % 2)
    {1: [1, 3], 0: [2, 4]}
    """
    groups: dict = {}
    for item in items:
        k = key(item)
        groups.setdefault(k, []).append(item)
    return groups
