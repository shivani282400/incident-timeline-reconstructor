# User Guide

## Prerequisites
- Python 3.9
- pip

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run the Application
```bash
python src/main/app.py
```

The API starts on `http://127.0.0.1:5000`.

## Available Endpoints

### Get Timeline
```bash
curl http://127.0.0.1:5000/timeline
```

### Get Incidents
```bash
curl http://127.0.0.1:5000/incidents
```

## Run Tests
```bash
pytest tests/unit tests/integration
```

## Run with Docker
```bash
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

## Monitoring Check
```bash
python3 monitoring/alerts/check_error_logs.py tests/testdata/sample_logs.txt
```
