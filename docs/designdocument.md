# Design Document

## Overview
The Incident Timeline Reconstructor is a modular Python project that transforms plain text application logs into structured event data and grouped incidents.

## Architecture
The project uses three simple modules:

### Parser
- Reads the log file
- Validates each line with regular expressions
- Converts timestamps into Python `datetime` objects

### Timeline
- Sorts events using parsed datetime values
- Builds a JSON-ready ordered timeline
- Groups incidents starting at `ERROR`
- Closes incidents when an `INFO` recovery event appears

### API
- Exposes `/timeline`
- Exposes `/incidents`
- Returns JSON responses
- Handles missing files and invalid logs safely

## DevOps Components
- Dockerfile for containerized execution
- docker-compose for local startup
- GitHub Actions workflow for automated testing
- Puppet manifest for basic host setup
- Monitoring script for alerting on `ERROR` lines

## Design Decisions
- Flask was chosen because it is lightweight and easy to understand
- No database is used because the project only reads log files
- The code uses standard Python modules where possible to keep the setup simple
