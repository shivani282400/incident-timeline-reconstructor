"""Integration tests for the Flask API."""

import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "main"))

from app import create_app  # noqa: E402


def test_api_returns_timeline_and_incidents(tmp_path):
    """API should return ordered events and grouped incidents."""
    log_file = tmp_path / "api.log"
    log_file.write_text(
        "2026-03-19 10:10:00 INFO Recovery complete\n"
        "2026-03-19 10:00:00 INFO Startup\n"
        "2026-03-19 10:05:00 ERROR Database unavailable\n"
        "2026-03-19 10:07:00 ERROR Timeout connecting to cache\n",
        encoding="utf-8",
    )

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    timeline_response = client.get("/timeline")
    incidents_response = client.get("/incidents")

    assert timeline_response.status_code == 200
    assert incidents_response.status_code == 200

    timeline_body = timeline_response.get_json()
    incidents_body = incidents_response.get_json()

    assert timeline_body["events"][0]["timestamp"] == "2026-03-19 10:00:00"
    assert timeline_body["events"][2]["timestamp"] == "2026-03-19 10:07:00"
    assert len(incidents_body["incidents"]) == 1
    assert incidents_body["incidents"][0]["status"] == "resolved"
    assert incidents_body["incidents"][0]["events"][0]["level"] == "ERROR"

    os.environ.pop("APP_LOG_FILE", None)


def test_api_handles_missing_file_gracefully():
    """API should return 404 when the configured log file is missing."""
    os.environ["APP_LOG_FILE"] = str(PROJECT_ROOT / "tests" / "testdata" / "missing.log")
    app = create_app()
    client = app.test_client()

    response = client.get("/timeline")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Log file not found"

    os.environ.pop("APP_LOG_FILE", None)


def test_api_handles_invalid_log_format(tmp_path):
    """API should return 400 for invalid log lines."""
    log_file = tmp_path / "invalid.log"
    log_file.write_text("invalid line\n", encoding="utf-8")

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    response = client.get("/incidents")

    assert response.status_code == 400
    assert "Invalid log format" in response.get_json()["error"]

    os.environ.pop("APP_LOG_FILE", None)


def test_api_returns_empty_timeline_for_empty_log_file(tmp_path):
    """API should return an empty timeline for an empty file."""
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    response = client.get("/timeline")

    assert response.status_code == 200
    assert response.get_json()["events"] == []

    os.environ.pop("APP_LOG_FILE", None)


def test_add_log_appends_new_entry(tmp_path):
    """POST /add-log should append a new log entry."""
    log_file = tmp_path / "add.log"
    log_file.write_text("2026-03-19 10:00:00 INFO Startup\n", encoding="utf-8")

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/add-log",
        json={
            "timestamp": "2026-03-19 11:00:00",
            "level": "error",
            "message": "New crash",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Log added successfully"
    assert "2026-03-19 11:00:00 ERROR New crash" in log_file.read_text(encoding="utf-8")

    os.environ.pop("APP_LOG_FILE", None)


def test_add_log_ignores_duplicates(tmp_path):
    """POST /add-log should not append duplicate entries."""
    log_file = tmp_path / "duplicate.log"
    log_file.write_text("2026-03-19 11:00:00 ERROR New crash\n", encoding="utf-8")

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/add-log",
        json={
            "timestamp": "2026-03-19 11:00:00",
            "level": "ERROR",
            "message": "New crash",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Duplicate log ignored"
    assert log_file.read_text(encoding="utf-8").count("2026-03-19 11:00:00 ERROR New crash") == 1

    os.environ.pop("APP_LOG_FILE", None)


def test_metrics_returns_expected_values(tmp_path):
    """GET /metrics should return incident metrics."""
    log_file = tmp_path / "metrics.log"
    log_file.write_text(
        "2026-03-19 10:00:00 INFO Startup\n"
        "2026-03-19 10:05:00 ERROR Database unavailable\n"
        "2026-03-19 10:10:00 INFO Recovery complete\n"
        "2026-03-19 10:15:00 ERROR Cache failure\n"
        "2026-03-19 10:20:00 INFO Cache restored\n",
        encoding="utf-8",
    )

    os.environ["APP_LOG_FILE"] = str(log_file)
    app = create_app()
    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.get_json() == {
        "total_incidents": 2,
        "total_errors": 2,
        "average_duration_seconds": 300,
        "longest_incident_seconds": 300,
    }

    os.environ.pop("APP_LOG_FILE", None)
