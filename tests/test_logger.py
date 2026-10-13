"""Tests for utils/logger.py"""
import logging
import pytest
from utils.logger import get_logger


def test_get_logger_returns_logger():
    log = get_logger("test.basic")
    assert isinstance(log, logging.Logger)


def test_get_logger_same_name_is_idempotent():
    log1 = get_logger("test.idempotent")
    log2 = get_logger("test.idempotent")
    assert log1 is log2


def test_get_logger_level_debug():
    log = get_logger("test.debug_level", level="DEBUG")
    assert log.level == logging.DEBUG


def test_get_logger_level_warning():
    log = get_logger("test.warn_level", level="WARNING")
    assert log.level == logging.WARNING


def test_get_logger_has_console_handler():
    log = get_logger("test.console")
    assert len(log.handlers) >= 1


def test_get_logger_file_handler(tmp_path):
    log_file = tmp_path / "app.log"
    log = get_logger("test.file_handler", log_file=log_file)
    assert log_file.parent.exists()
    handlers = [type(h).__name__ for h in log.handlers]
    assert "RotatingFileHandler" in handlers


def test_logger_can_log_without_error(caplog):
    log = get_logger("test.log_output", level="DEBUG")
    log.info("hello from test")


def test_file_setup_failure_can_be_retried(tmp_path):
    name = "test.failed_setup_retry"
    blocker = tmp_path / "parent"
    blocker.write_text("not a directory")
    with pytest.raises(OSError):
        get_logger(name, log_file=blocker / "app.log")
    assert logging.getLogger(name).handlers == []
    log = get_logger(name, log_file=tmp_path / "valid.log")
    try:
        log.info("retry succeeded")
        assert "retry succeeded" in (tmp_path / "valid.log").read_text()
    finally:
        for handler in log.handlers[:]:
            handler.close()
            log.removeHandler(handler)
