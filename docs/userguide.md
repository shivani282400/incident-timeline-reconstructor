# User Guide

## 1. Prerequisites

- Python 3.9
- pip
- Docker and Docker Compose (optional)

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the Project

Start the Flask application:

```bash
python3 src/main/app.py
```

Open the dashboard:

```text
http://127.0.0.1:5001/
```

## 4. Using the Dashboard

The dashboard displays:

- a timeline table with timestamp, level, and message
- color-coded severity values
- incident cards showing start time, end time, status, and event count
- top-level summary metrics for incidents and errors

## 5. Using the APIs

### Get All Timeline Events

```bash
curl http://127.0.0.1:5001/timeline
```

### Filter Timeline by Severity

```bash
curl http://127.0.0.1:5001/timeline?level=ERROR
```

### Get Incidents

```bash
curl http://127.0.0.1:5001/incidents
```

### Get Metrics

```bash
curl http://127.0.0.1:5001/metrics
```

### Add a New Log Entry

```bash
curl -X POST http://127.0.0.1:5001/add-log \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2026-03-25 11:00:00","level":"ERROR","message":"New crash"}'
```

If the same log already exists, the API returns:

```json
{
  "message": "Duplicate log ignored"
}
```

## 6. Run with Docker

```bash
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

Open:

```text
http://127.0.0.1:5001/
```

## 7. Run Tests

```bash
python3 -m pytest tests/unit tests/integration
```

## 8. Run Monitoring

Execute the monitoring script manually:

```bash
python3 monitoring/alerts/check_error_logs.py tests/testdata/sample_logs.txt
```

Expected behavior:

- returns `0` when no `ERROR` logs are present
- returns `2` when one or more `ERROR` logs are found

## 9. Configuration

Default settings are stored in:

```text
src/main/config/config.yaml
```

The log file path can also be overridden with:

```bash
export APP_LOG_FILE=/absolute/path/to/logfile.txt
```
