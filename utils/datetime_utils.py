"""Date and time utilities for operations and automation.

Usage
-----
>>> from utils.datetime_utils import now_utc, parse_date, humanize_delta
"""

from __future__ import annotations
from datetime import datetime, timezone, timedelta


def now_utc() -> datetime:
    """Return current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """Parse a date string into a datetime object."""
    return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)


def humanize_delta(seconds: float) -> str:
    """Convert seconds to human-readable duration.

    >>> humanize_delta(3661)
    '1h 1m 1s'
    """
    seconds = int(seconds)
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    parts = []
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    if s or not parts: parts.append(f"{s}s")
    return " ".join(parts)


def timestamp_ms() -> int:
    """Return current UTC timestamp in milliseconds."""
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def is_market_hours(dt: datetime | None = None) -> bool:
    """Check if given time is within NYSE market hours (9:30–16:00 ET).

    Note: does not account for holidays.
    """
    from zoneinfo import ZoneInfo
    et = ZoneInfo("America/New_York")
    dt = dt or datetime.now(et)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=et)
    dt_et = dt.astimezone(et)
    if dt_et.weekday() >= 5:
        return False
    open_time = dt_et.replace(hour=9, minute=30, second=0, microsecond=0)
    close_time = dt_et.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_time <= dt_et <= close_time
