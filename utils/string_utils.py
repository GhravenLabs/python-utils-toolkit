"""Handy string manipulation utilities.

Usage
-----
>>> from utils.string_utils import slugify, truncate, camel_to_snake

>>> slugify("Hello World!")        # "hello-world"
>>> truncate("long text...", 10)   # "long te..."
>>> camel_to_snake("camelCase")    # "camel_case"
"""

from __future__ import annotations

import re
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """Convert *text* to a URL-safe slug.

    Strips accents, lowercases, replaces spaces and punctuation with
    *separator*, and collapses consecutive separators.

    >>> slugify("Hello, World!")
    'hello-world'
    >>> slugify("Ångström Units", separator="_")
    'angstrom_units'
    """
    # Normalize unicode → decompose accented chars
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # Replace non-alphanumeric characters with separator
    return separator.join(re.findall(r"[a-z0-9]+", text))


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate *text* to *max_length* characters, appending *suffix* if cut.

    >>> truncate("Hello World", 8)
    'Hello...'
    >>> truncate("Hi", 10)
    'Hi'
    """
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 0:
        raise ValueError("max_length must be a nonnegative integer")
    if len(text) <= max_length:
        return text
    cut = max_length - len(suffix)
    if cut <= 0:
        return suffix[:max_length]
    return text[:cut] + suffix


def camel_to_snake(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case.

    >>> camel_to_snake("camelCase")
    'camel_case'
    >>> camel_to_snake("HTTPSRequest")
    'https_request'
    """
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase.

    >>> snake_to_camel("hello_world")
    'helloWorld'
    """
    parts = name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def indent(text: str, spaces: int = 4) -> str:
    """Indent every line of *text* by *spaces* spaces."""
    prefix = " " * spaces
    return "\n".join(prefix + line for line in text.splitlines())


def remove_prefix(text: str, prefix: str) -> str:
    """Remove *prefix* from the start of *text* if present."""
    return text[len(prefix):] if text.startswith(prefix) else text


def remove_suffix(text: str, suffix: str) -> str:
    """Remove *suffix* from the end of *text* if present."""
    return text[:-len(suffix)] if suffix and text.endswith(suffix) else text
