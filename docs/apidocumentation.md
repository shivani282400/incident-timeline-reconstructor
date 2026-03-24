# API Documentation

## Base URL

```text
http://127.0.0.1:5001
```

---

## 1. GET /timeline

### Description
Returns all parsed log events ordered by timestamp.

### Request

```bash
curl http://127.0.0.1:5001/timeline
```

### Response Example

```json
{
  "events": [
    {
      "timestamp": "2026-03-19 09:00:00",
      "level": "INFO",
      "message": "Service boot initiated"
    },
    {
      "timestamp": "2026-03-19 09:05:00",
      "level": "ERROR",
      "message": "API gateway timeout"
    }
  ]
}
```

---

## 2. GET /timeline?level=ERROR

### Description
Returns only events that match the requested severity level. Filtering is case-insensitive.

### Request

```bash
curl http://127.0.0.1:5001/timeline?level=ERROR
```

### Response Example

```json
{
  "events": [
    {
      "timestamp": "2026-03-19 09:05:00",
      "level": "ERROR",
      "message": "API gateway timeout"
    },
    {
      "timestamp": "2026-03-19 09:06:30",
      "level": "ERROR",
      "message": "Worker queue stalled"
    }
  ]
}
```

---

## 3. GET /incidents

### Description
Returns grouped incidents. An incident starts at `ERROR` and closes on `INFO` recovery.

### Request

```bash
curl http://127.0.0.1:5001/incidents
```

### Response Example

```json
{
  "incidents": [
    {
      "start_time": "2026-03-19 09:05:00",
      "end_time": "2026-03-19 09:10:00",
      "status": "resolved",
      "event_count": 4,
      "duration_seconds": 300,
      "events": [
        {
          "timestamp": "2026-03-19 09:05:00",
          "level": "ERROR",
          "message": "API gateway timeout"
        },
        {
          "timestamp": "2026-03-19 09:06:30",
          "level": "ERROR",
          "message": "Worker queue stalled"
        }
      ]
    }
  ]
}
```

---

## 4. GET /metrics

### Description
Returns operational metrics based on the current log file and derived incidents.

### Request

```bash
curl http://127.0.0.1:5001/metrics
```

### Response Example

```json
{
  "total_incidents": 2,
  "total_errors": 5,
  "average_duration_seconds": 240,
  "longest_incident_seconds": 300
}
```

---

## 5. POST /add-log

### Description
Adds a new log entry to the configured log file. If the same line already exists, the request is ignored.

### Request

```bash
curl -X POST http://127.0.0.1:5001/add-log \
  -H "Content-Type: application/json" \
  -d '{
        "timestamp": "2026-03-25 11:00:00",
        "level": "ERROR",
        "message": "New crash"
      }'
```

### Request Body

```json
{
  "timestamp": "2026-03-25 11:00:00",
  "level": "ERROR",
  "message": "New crash"
}
```

### Success Response Example

```json
{
  "message": "Log added successfully"
}
```

### Duplicate Response Example

```json
{
  "message": "Duplicate log ignored"
}
```

### Validation Error Example

```json
{
  "error": "timestamp, level, and message are required"
}
```
