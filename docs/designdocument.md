# Design Document

## 1. System Overview

Incident Timeline Reconstructor is a modular Flask application that transforms plain text logs into structured operational insights. It reads log entries, sorts them chronologically, detects incident windows, exposes REST APIs, and renders a simple dashboard for monitoring.

## 2. High-Level Architecture

```text
Log File
   |
   v
Parser Module
   |
   v
Timeline Module
   |
   +--> REST API
   |
   +--> HTML Dashboard
   |
   +--> Monitoring Scripts
   |
   v
Alerts / Operations Response
```

## 3. Module Design

### Parser Module
File: `src/main/parser.py`

Responsibilities:

- read the configured log file
- validate log lines using regular expressions
- parse timestamps into Python `datetime` objects
- raise clear errors for invalid log lines or missing files

Input format:

```text
YYYY-MM-DD HH:MM:SS LEVEL MESSAGE
```

Output format:

```python
{
    "timestamp": datetime(...),
    "level": "ERROR",
    "message": "Database unavailable"
}
```

### Timeline Module
File: `src/main/timeline.py`

Responsibilities:

- sort structured events by timestamp
- serialize events into JSON-ready dictionaries
- group incidents starting at `ERROR`
- close incidents when `INFO` recovery appears
- calculate incident metadata such as event count and duration

### API Module
File: `src/main/app.py`

Responsibilities:

- load configuration from `config.yaml`
- expose operational APIs
- provide a dashboard route
- support log ingestion through `POST /add-log`
- prevent duplicate log entries
- provide metrics for observability

Main endpoints:

- `GET /`
- `GET /timeline`
- `GET /incidents`
- `GET /metrics`
- `POST /add-log`

### Monitoring Module
Files:

- `monitoring/alerts/check_error_logs.py`
- `monitoring/nagios/nagios.cfg`

Responsibilities:

- scan log files for `ERROR` entries
- return monitoring-friendly exit codes
- provide a Nagios-compatible command definition

## 4. Data Flow

1. The application reads the log file path from configuration or environment override.
2. The parser converts raw log lines into structured event dictionaries.
3. The timeline module sorts events and groups incidents.
4. API routes return JSON responses or render HTML output.
5. Monitoring scripts inspect the same log source and raise alerts when failures are present.

## 5. DevOps Components

### Docker

- `infrastructure/docker/Dockerfile` packages the Flask application
- `infrastructure/docker/docker-compose.yml` runs the service locally on port `5001`

### CI/CD

- `.github/workflows/cicd.yml` installs dependencies and runs tests automatically
- validates parser, timeline, and API behavior before integration

### Puppet

- `infrastructure/puppet/init.pp` installs Python and provisions example monitoring files
- demonstrates basic infrastructure-as-code usage for a DevOps course project

## 6. Design Decisions

- Flask is used for simplicity and readability
- plain text logs are used to keep the project lightweight
- no database is required because all processing is file-based
- Docker and GitHub Actions are included to demonstrate deployment and CI practices
- monitoring is intentionally simple but realistic enough for educational use
