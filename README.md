# Incident Timeline Reconstructor

Incident Timeline Reconstructor is a Flask-based DevOps project that reads application logs, reconstructs event timelines, detects incidents, exposes REST APIs, and provides a lightweight monitoring dashboard. The project is designed to demonstrate backend engineering, observability, CI/CD, containerization, and infrastructure automation in one cohesive workflow.

## Features

- Parse log lines in the format `YYYY-MM-DD HH:MM:SS LEVEL MESSAGE`
- Build a chronological timeline of events
- Detect incidents from `ERROR` until `INFO` recovery
- Calculate incident metrics such as total incidents, total errors, average duration, and longest incident
- Add new log entries through an API endpoint
- Prevent duplicate log entries
- Display a simple HTML dashboard for live monitoring
- Run monitoring checks through Python scripts and Nagios configuration
- Containerize the application with Docker and Docker Compose
- Automate test execution with GitHub Actions
- Manage environment setup through Puppet

## Architecture

```text
Logs -> Parser -> Timeline -> API -> Monitoring -> Alerts
```

- `Logs`: input data stored in a plain text log file
- `Parser`: validates each log line and converts timestamps into structured events
- `Timeline`: sorts events and groups incidents
- `API`: exposes endpoints for timeline, incidents, metrics, and log ingestion
- `Monitoring`: scans logs for failures and reports health
- `Alerts`: surfaces failures through monitoring integrations such as Nagios

## Tech Stack

- Python 3.9
- Flask
- Docker
- GitHub Actions
- Puppet
- Python monitoring scripts
- Nagios configuration

## Project Structure

```text
.
├── .github/workflows/
├── docs/
├── infrastructure/
│   ├── docker/
│   └── puppet/
├── monitoring/
│   ├── alerts/
│   └── nagios/
├── src/main/
├── templates/
└── tests/
```

## Installation

1. Clone the repository.
2. Move into the project directory.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Start the Flask application:

```bash
python3 src/main/app.py
```

Open the dashboard in a browser:

```text
http://127.0.0.1:5001/
```

## Run with Docker

Build and start the service:

```bash
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

The application will be available on:

```text
http://127.0.0.1:5001/
```

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI for timeline and incidents |
| `/timeline` | GET | Returns all parsed events |
| `/timeline?level=ERROR` | GET | Returns events filtered by level |
| `/incidents` | GET | Returns grouped incidents |
| `/metrics` | GET | Returns incident and error metrics |
| `/add-log` | POST | Adds a new log entry if it is not a duplicate |

## Example API Usage

Get the full timeline:

```bash
curl http://127.0.0.1:5001/timeline
```

Get only error events:

```bash
curl http://127.0.0.1:5001/timeline?level=ERROR
```

Add a new log entry:

```bash
curl -X POST http://127.0.0.1:5001/add-log \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2026-03-25 11:00:00","level":"ERROR","message":"New crash"}'
```

## Monitoring

Run the monitoring check manually:

```bash
python3 monitoring/alerts/check_error_logs.py tests/testdata/sample_logs.txt
```

## CI/CD

The GitHub Actions workflow:

- installs Python dependencies
- runs unit and integration tests

Workflow file:

```text
.github/workflows/cicd.yml
```
