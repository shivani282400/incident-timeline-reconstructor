import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from parser import LogParseError, parse_log_file
from timeline import build_incidents, build_timeline


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "src" / "main" / "config" / "config.yaml"


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger(__name__)


def load_config():
    config = {
        "log_file": "tests/testdata/sample_logs.txt",
        "port": 5001,
    }

    if not CONFIG_PATH.exists():
        return config

    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        for raw_line in config_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "port":
                try:
                    config[key] = int(value)
                except ValueError:
                    continue
            else:
                config[key] = value

    return config


def create_app():
    config = load_config()
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

    configured_log_file = os.getenv("APP_LOG_FILE", config.get("log_file", "tests/testdata/sample_logs.txt"))
    log_file_path = Path(configured_log_file)
    if not log_file_path.is_absolute():
        log_file_path = (BASE_DIR / log_file_path).resolve()

    app.config["LOG_FILE"] = str(log_file_path)
    app.config["PORT"] = config.get("port", 5001)

    @app.route("/", methods=["GET"])
    def home():
        try:
            LOGGER.info("Parsing logs for dashboard")
            events = parse_log_file(app.config["LOG_FILE"])
            timeline = build_timeline(events)
            LOGGER.info("Building incidents for dashboard")
            incidents = build_incidents(events)
            total_incidents = len(incidents)
            total_errors = sum(1 for event in events if event["level"] == "ERROR")

            return render_template(
                "index.html",
                timeline=timeline,
                incidents=incidents,
                total_incidents=total_incidents,
                total_errors=total_errors,
            )
        except FileNotFoundError:
            return "<h1>Log file not found</h1>", 404
        except LogParseError as error:
            return f"<h1>Invalid log file</h1><p>{error}</p>", 400

    @app.route("/timeline", methods=["GET"])
    def get_timeline():
        try:
            LOGGER.info("Parsing logs for timeline")
            events = parse_log_file(app.config["LOG_FILE"])
            level = request.args.get("level")

            if level:
                normalized_level = level.upper()
                events = [event for event in events if event["level"] == normalized_level]

            return jsonify({"events": build_timeline(events)}), 200
        except FileNotFoundError:
            return jsonify({"error": "Log file not found", "events": []}), 404
        except LogParseError as error:
            return jsonify({"error": str(error), "events": []}), 400

    @app.route("/incidents", methods=["GET"])
    def get_incidents():
        try:
            LOGGER.info("Parsing logs for incidents")
            events = parse_log_file(app.config["LOG_FILE"])
            LOGGER.info("Building incidents")
            return jsonify({"incidents": build_incidents(events)}), 200
        except FileNotFoundError:
            return jsonify({"error": "Log file not found", "incidents": []}), 404
        except LogParseError as error:
            return jsonify({"error": str(error), "incidents": []}), 400

    @app.route("/metrics", methods=["GET"])
    def get_metrics():
        try:
            LOGGER.info("Parsing logs for metrics")
            events = parse_log_file(app.config["LOG_FILE"])
            LOGGER.info("Building incidents for metrics")
            incidents = build_incidents(events)
            total_errors = sum(1 for event in events if event["level"] == "ERROR")

            durations = [
                incident["duration_seconds"]
                for incident in incidents
                if incident.get("duration_seconds") is not None
            ]

            average_duration = int(sum(durations) / len(durations)) if durations else 0
            longest_incident = max(durations) if durations else 0

            return jsonify(
                {
                    "total_incidents": len(incidents),
                    "total_errors": total_errors,
                    "average_duration_seconds": average_duration,
                    "longest_incident_seconds": longest_incident,
                }
            ), 200
        except FileNotFoundError:
            return jsonify({"error": "Log file not found"}), 404
        except LogParseError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/add-log", methods=["POST"])
    def add_log():
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Invalid input"}), 400

        timestamp = payload.get("timestamp")
        level = payload.get("level")
        message = payload.get("message")

        if not timestamp or not level or not message:
            return jsonify({"error": "timestamp, level, and message are required"}), 400

        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"error": "Invalid timestamp format"}), 400

        normalized_level = str(level).upper()
        log_line = f"{timestamp} {normalized_level} {message}"

        try:
            with open(app.config["LOG_FILE"], "r", encoding="utf-8") as log_file:
                existing_lines = {line.strip() for line in log_file}
        except FileNotFoundError:
            existing_lines = set()
        except OSError:
            return jsonify({"error": "Unable to read log file"}), 500

        if log_line in existing_lines:
            LOGGER.info("Duplicate log ignored")
            return jsonify({"message": "Duplicate log ignored"}), 200

        try:
            with open(app.config["LOG_FILE"], "a", encoding="utf-8") as log_file:
                log_file.write(f"{log_line}\n")
        except OSError:
            return jsonify({"error": "Unable to write log file"}), 500

        LOGGER.info("New log added")
        return jsonify({"message": "Log added successfully"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"])
