"""Timeline and incident-building utilities."""

from typing import Dict, List


def sort_events(events: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Sort structured log events by their datetime timestamp."""
    return sorted(events, key=lambda item: item["timestamp"])


def serialize_event(event: Dict[str, object]) -> Dict[str, str]:
    """Convert a structured event into a JSON-ready dictionary."""
    return {
        "timestamp": event["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
        "level": event["level"],
        "message": event["message"],
    }


def build_timeline(events: List[Dict[str, object]]) -> List[Dict[str, str]]:
    """Build a chronologically ordered timeline from parsed events."""
    ordered_events = sort_events(events)
    return [serialize_event(event) for event in ordered_events]


def build_incidents(events: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Group incidents from the first ERROR until the next INFO recovery."""
    incidents = []
    current_incident = None

    for event in sort_events(events):
        if event["level"] == "ERROR":
            if current_incident is None:
                current_incident = {
                    "start_time": event["timestamp"],
                    "end_time": None,
                    "status": "open",
                    "events": [],
                }
            current_incident["events"].append(event)
            continue

        if current_incident is None:
            continue

        current_incident["events"].append(event)
        if event["level"] == "INFO":
            current_incident["end_time"] = event["timestamp"]
            current_incident["status"] = "resolved"
            incidents.append(_serialize_incident(current_incident))
            current_incident = None

    if current_incident is not None:
        incidents.append(_serialize_incident(current_incident))

    return incidents


def _serialize_incident(incident: Dict[str, object]) -> Dict[str, object]:
    """Convert an incident into a JSON-ready dictionary."""
    return {
        "start_time": incident["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": (
            incident["end_time"].strftime("%Y-%m-%d %H:%M:%S")
            if incident["end_time"] is not None
            else None
        ),
        "status": incident["status"],
        "event_count": len(incident["events"]),
        "duration_seconds": (
            int((incident["end_time"] - incident["start_time"]).total_seconds())
            if incident["end_time"] is not None
            else None
        ),
        "events": [serialize_event(event) for event in incident["events"]],
    }
