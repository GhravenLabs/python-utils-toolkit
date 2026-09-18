"""Number formatting and financial math utilities."""

from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP


def format_currency(amount: float, symbol: str = "$", decimals: int = 2) -> str:
    """Format a number as currency string.

    >>> format_currency(1234567.89)
    '$1,234,567.89'
    """
    return f"{symbol}{amount:,.{decimals}f}"


def round_to_tick(price: float, tick_size: float) -> float:
    """Round price to nearest tick size (for exchange order placement).

    >>> round_to_tick(0.12345, 0.0001)
    0.1235
    """
    tick = Decimal(str(tick_size))
    price_d = Decimal(str(price))
    return float((price_d / tick).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * tick)


def pct_change(old: float, new: float) -> float:
    """Calculate percentage change between two values.

    >>> pct_change(100, 110)
    10.0
    """
    if old == 0:
        return 0.0
    return ((new - old) / abs(old)) * 100


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max.

    >>> clamp(15, 0, 10)
    10
    """
    if min_val > max_val:
        raise ValueError("min_val must not exceed max_val")
    return max(min_val, min(max_val, value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide safely, returning *default* on zero division."""
    if denominator == 0:
        return default
    return numerator / denominator
