"""Unit tests for log parsing."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "main"))

from parser import LogParseError, parse_log_file  # noqa: E402


def test_parse_log_file_returns_structured_events(tmp_path):
    """Parser should return structured events for valid log lines."""
    log_file = tmp_path / "parser.log"
    log_file.write_text(
        "2026-03-19 10:00:00 INFO Service started\n"
        "2026-03-19 10:05:00 ERROR Database unavailable\n",
        encoding="utf-8",
    )

    events = parse_log_file(str(log_file))

    assert len(events) == 2
    assert events[0]["level"] == "INFO"
    assert events[1]["message"] == "Database unavailable"


def test_parse_log_file_raises_for_invalid_lines(tmp_path):
    """Parser should reject log lines that do not match the format."""
    log_file = tmp_path / "invalid.log"
    log_file.write_text("bad log line\n", encoding="utf-8")

    with pytest.raises(LogParseError):
        parse_log_file(str(log_file))


def test_parse_log_file_raises_for_invalid_timestamp(tmp_path):
    """Parser should reject log lines with invalid datetime values."""
    log_file = tmp_path / "invalid-time.log"
    log_file.write_text("2026-99-19 10:00:00 ERROR Invalid date\n", encoding="utf-8")

    with pytest.raises(LogParseError):
        parse_log_file(str(log_file))


def test_parse_log_file_returns_empty_list_for_empty_file(tmp_path):
    """Parser should return an empty list for an empty log file."""
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    assert parse_log_file(str(log_file)) == []


def test_parse_log_file_raises_for_missing_file(tmp_path):
    """Parser should raise FileNotFoundError when the log file is missing."""
    missing_file = tmp_path / "missing.log"

    with pytest.raises(FileNotFoundError):
        parse_log_file(str(missing_file))
