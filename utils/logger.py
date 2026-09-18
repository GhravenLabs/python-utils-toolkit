"""One-call structured logging setup with colour output and file rotation.

Usage
-----
>>> log = get_logger("my_app", level="DEBUG", log_file="app.log")
>>> log.info("Starting up")
>>> log.warning("Rate limit hit", extra={"endpoint": "/prices"})
"""

from __future__ import annotations

import copy
import logging
import logging.handlers
import sys
from pathlib import Path


_COLOURS = {
    "DEBUG": "\033[36m",    # cyan
    "INFO": "\033[32m",     # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",    # red
    "CRITICAL": "\033[35m", # magenta
    "RESET": "\033[0m",
}


class _ColourFormatter(logging.Formatter):
    """Add ANSI colour codes to console log levels."""

    FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        record = copy.copy(record)
        colour = _COLOURS.get(record.levelname, _COLOURS["RESET"])
        reset = _COLOURS["RESET"]
        record.levelname = f"{colour}{record.levelname}{reset}"
        return super().format(record)


def get_logger(
    name: str,
    level: str = "INFO",
    log_file: str | Path | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    """Create or retrieve a logger with console + optional rotating file handler.

    Parameters
    ----------
    name:
        Logger name (appears in every log line).
    level:
        Minimum log level — ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, etc.
    log_file:
        Path for a rotating file handler. ``None`` disables file logging.
    max_bytes:
        Maximum size of a single log file before rotation (default 10 MB).
    backup_count:
        Number of rotated files to keep.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    log = logging.getLogger(name)
    if log.handlers:
        return log  # already configured

    log.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler with colour
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(_ColourFormatter(_ColourFormatter.FMT))
    log.addHandler(console)

    # Rotating file handler
    if log_file is not None:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
        )
        log.addHandler(file_handler)

    return log
