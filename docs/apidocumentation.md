# API Documentation

## Base URL
`http://127.0.0.1:5000`

## GET /timeline
Returns all valid log events ordered by timestamp.

### Example Response
```json
{
  "events": [
    {
      "timestamp": "2026-03-19 09:00:00",
      "level": "INFO",
      "message": "Service boot initiated"
    }
  ]
}
```

## GET /incidents
Returns grouped incidents.

### Incident Rules
- An incident starts when an `ERROR` event appears
- Additional events are attached to the current incident
- The incident ends when an `INFO` recovery event appears
- If no recovery appears, the incident stays open

### Example Response
```json
{
  "incidents": [
    {
      "start_time": "2026-03-19 09:05:00",
      "end_time": "2026-03-19 09:10:00",
      "status": "resolved",
      "events": [
        {
          "timestamp": "2026-03-19 09:05:00",
          "level": "ERROR",
          "message": "API gateway timeout"
        }
      ]
    }
  ]
}
```

## Error Responses
- `404` when the log file does not exist
- `400` when the log format is invalid
- `500` when the log file cannot be read
