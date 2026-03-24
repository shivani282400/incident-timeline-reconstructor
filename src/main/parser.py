"""Log parsing utilities for the incident timeline application."""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) (?P<message>.+)$"
)


class LogParseError(Exception):
    """Raised when a log line does not match the expected format."""


def parse_log_line(line: str, line_number: int) -> Dict[str, object]:
    """Parse one log line into a structured event dictionary."""
    stripped_line = line.strip()
    if not stripped_line:
        raise LogParseError(f"Invalid log format at line {line_number}: empty line")

    match = LOG_PATTERN.match(stripped_line)
    if not match:
        raise LogParseError(f"Invalid log format at line {line_number}: {stripped_line}")

    try:
        timestamp = datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise LogParseError(
            f"Invalid timestamp at line {line_number}: {match.group('timestamp')}"
        ) from error

    event = {
        "timestamp": timestamp,
        "level": match.group("level"),
        "message": match.group("message"),
    }
    LOGGER.debug("Parsed log line %s into event %s", line_number, event)
    return event


def parse_log_file(file_path: str) -> List[Dict[str, object]]:
    """Parse a log file and return all valid events."""
    path = Path(file_path)

    if not path.exists():
        LOGGER.error("Log file not found: %s", file_path)
        raise FileNotFoundError(f"Log file not found: {file_path}")

    events: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            if not line.strip():
                continue
            events.append(parse_log_line(line, line_number))

    LOGGER.info("Parsed %s events from %s", len(events), file_path)
    return events
