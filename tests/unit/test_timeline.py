"""Unit tests for timeline and incident logic."""

from datetime import datetime
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "main"))

from timeline import build_incidents, build_timeline  # noqa: E402


def _event(timestamp, level, message):
    """Create a structured event for testing."""
    return {
        "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message,
    }


def test_build_timeline_sorts_events_by_datetime():
    """Timeline should always be sorted chronologically."""
    events = [
        _event("2026-03-19 10:10:00", "INFO", "Recovered"),
        _event("2026-03-19 10:00:00", "INFO", "Started"),
        _event("2026-03-19 10:05:00", "ERROR", "Failed"),
    ]

    timeline = build_timeline(events)

    assert [item["timestamp"] for item in timeline] == [
        "2026-03-19 10:00:00",
        "2026-03-19 10:05:00",
        "2026-03-19 10:10:00",
    ]


def test_build_incidents_groups_until_info_recovery():
    """Incident detection should start on ERROR and end on INFO."""
    events = [
        _event("2026-03-19 10:10:00", "INFO", "Recovered"),
        _event("2026-03-19 10:05:00", "ERROR", "Database unavailable"),
        _event("2026-03-19 10:07:00", "WARNING", "Retrying"),
    ]

    incidents = build_incidents(events)

    assert len(incidents) == 1
    assert incidents[0]["start_time"] == "2026-03-19 10:05:00"
    assert incidents[0]["end_time"] == "2026-03-19 10:10:00"
    assert incidents[0]["status"] == "resolved"


def test_build_incidents_keeps_open_incident_without_recovery():
    """Incident should stay open when no INFO recovery appears."""
    events = [
        _event("2026-03-19 10:05:00", "ERROR", "Database unavailable"),
        _event("2026-03-19 10:07:00", "WARNING", "Retrying"),
    ]

    incidents = build_incidents(events)

    assert len(incidents) == 1
    assert incidents[0]["status"] == "open"
    assert incidents[0]["end_time"] is None
