"""Typed environment variable / .env file loader.

Usage
-----
>>> from utils.env import Env
>>> env = Env()          # reads from os.environ + .env if present
>>> token = env.str("API_KEY")
>>> port  = env.int("PORT", default=8080)
>>> debug = env.bool("DEBUG", default=False)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


class Env:
    """Typed accessor for environment variables.

    On construction, loads a ``.env`` file from *dotenv_path* (if present)
    without overwriting already-set environment variables — same behaviour
    as ``python-dotenv``\'s ``load_dotenv(override=False)``, implemented
    here with zero extra dependencies.

    Parameters
    ----------
    dotenv_path:
        Path to the ``.env`` file. Defaults to ``.env`` in the working directory.
    """

    def __init__(self, dotenv_path: str | Path = ".env") -> None:
        self._load_dotenv(Path(dotenv_path))

    @staticmethod
    def _load_dotenv(path: Path) -> None:
        if not path.exists():
            return
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                # Do not overwrite already-set variables
                os.environ.setdefault(key, value)

    def str(self, key: str, default: Optional[str] = None) -> str:
        """Return *key* as a string.

        Raises ``KeyError`` when the key is absent and no *default* is given.
        """
        val = os.environ.get(key, default)
        if val is None:
            raise KeyError(f"Required environment variable {key!r} is not set.")
        return val

    def int(self, key: str, default: Optional[int] = None) -> int:
        """Return *key* as an integer."""
        raw = os.environ.get(key)
        if raw is None:
            if default is not None:
                return default
            raise KeyError(f"Required environment variable {key!r} is not set.")
        try:
            return int(raw)
        except ValueError as exc:
            raise ValueError(f"Environment variable {key!r} must be an integer, got {raw!r}") from exc

    def float(self, key: str, default: Optional[float] = None) -> float:
        """Return *key* as a float."""
        raw = os.environ.get(key)
        if raw is None:
            if default is not None:
                return default
            raise KeyError(f"Required environment variable {key!r} is not set.")
        try:
            return float(raw)
        except ValueError as exc:
            raise ValueError(f"Environment variable {key!r} must be a float, got {raw!r}") from exc

    def bool(self, key: str, default: Optional[bool] = None) -> bool:
        """Return *key* as a boolean.

        Truthy strings: ``"1"``, ``"true"``, ``"yes"``, ``"on"`` (case-insensitive).
        Everything else is ``False``.
        """
        raw = os.environ.get(key)
        if raw is None:
            if default is not None:
                return default
            raise KeyError(f"Required environment variable {key!r} is not set.")
        return raw.strip().lower() in ("1", "true", "yes", "on")

    def list(self, key: str, separator: str = ",", default: Optional[list] = None) -> list[str]:
        """Return *key* as a list of strings split by *separator*."""
        raw = os.environ.get(key)
        if raw is None:
            return default if default is not None else []
        return [item.strip() for item in raw.split(separator) if item.strip()]
