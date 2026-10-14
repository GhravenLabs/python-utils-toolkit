"""Tests for utils/file_helpers.py"""
import json
import os
import pytest
from pathlib import Path
from utils.file_helpers import (
    read_text, write_text, read_json, write_json, atomic_write, ensure_dir, file_size
)


@pytest.fixture
def tmp(tmp_path):
    return tmp_path


def test_write_and_read_text(tmp):
    p = tmp / "hello.txt"
    write_text(p, "hello world")
    assert read_text(p) == "hello world"


def test_read_text_missing_returns_empty(tmp):
    assert read_text(tmp / "nonexistent.txt") == ""


def test_write_text_creates_parent_dirs(tmp):
    p = tmp / "deep" / "dir" / "file.txt"
    write_text(p, "data")
    assert p.read_text() == "data"


def test_write_and_read_json(tmp):
    p = tmp / "data.json"
    data = {"key": "value", "num": 42}
    write_json(p, data)
    loaded = read_json(p)
    assert loaded == data


def test_read_json_missing_returns_default(tmp):
    assert read_json(tmp / "missing.json", default={}) == {}
    assert read_json(tmp / "missing.json") is None


def test_read_json_invalid_raises(tmp):
    p = tmp / "bad.json"
    p.write_text("not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        read_json(p)


def test_atomic_write(tmp):
    p = tmp / "atomic.txt"
    atomic_write(p, "safe content")
    assert p.read_text(encoding="utf-8") == "safe content"


def test_atomic_write_flushes_content_before_replace(tmp, monkeypatch):
    events = []
    real_replace = os.replace
    monkeypatch.setattr(os, "fsync", lambda fd: events.append("fsync"))
    monkeypatch.setattr(os, "replace", lambda source, target: (
        events.append("replace"), real_replace(source, target)
    )[-1])
    atomic_write(tmp / "durable.txt", "complete")
    assert events == ["fsync", "replace"]


def test_atomic_write_no_temp_file_left(tmp):
    p = tmp / "out.txt"
    atomic_write(p, "data")
    tmp_files = [f for f in tmp.iterdir() if f.name.startswith(".tmp_")]
    assert tmp_files == []


def test_ensure_dir(tmp):
    d = tmp / "new" / "nested" / "dir"
    result = ensure_dir(d)
    assert result == d
    assert d.is_dir()


def test_file_size_existing(tmp):
    p = tmp / "f.txt"
    p.write_text("hello", encoding="utf-8")
    assert file_size(p) == 5


def test_file_size_missing(tmp):
    assert file_size(tmp / "nope.txt") == 0
