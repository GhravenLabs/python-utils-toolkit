"""Safe file read/write utilities with atomic saves.

Usage
-----
>>> from utils.file_helpers import read_json, write_json, atomic_write

>>> data = read_json("config.json", default={})
>>> write_json("config.json", {"key": "value"})
>>> atomic_write("output.txt", "hello world")
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Read a text file, returning empty string if it doesn't exist."""
    try:
        return Path(path).read_text(encoding=encoding)
    except FileNotFoundError:
        return ""


def write_text(path: str | Path, content: str, encoding: str = "utf-8") -> None:
    """Write text to a file, creating parent directories as needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


def read_json(path: str | Path, default: Any = None) -> Any:
    """Read a JSON file, returning *default* if the file doesn't exist."""
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e


def write_json(path: str | Path, data: Any, indent: int = 2) -> None:
    """Serialize first, then atomically replace JSON; create parent directories."""
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    atomic_write(path, content)


def atomic_write(path: str | Path, content: str, encoding: str = "utf-8") -> None:
    """Write content atomically using a temp file + rename.

    Prevents partial writes — if the process is interrupted the original
    file is never corrupted.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(dir=p.parent, prefix=".tmp_")
    try:
        with os.fdopen(tmp_fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_path, p)
    except Exception:
        os.unlink(tmp_path)
        raise


def ensure_dir(path: str | Path) -> Path:
    """Create directory (and parents) if it doesn't exist. Returns the Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def file_size(path: str | Path) -> int:
    """Return file size in bytes, or 0 if file doesn't exist."""
    try:
        return Path(path).stat().st_size
    except FileNotFoundError:
        return 0
