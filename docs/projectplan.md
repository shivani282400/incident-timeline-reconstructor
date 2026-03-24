# Project Plan

## Project Title
Incident Timeline Reconstructor

## Goal
Build a small Flask application that reads log files, creates an ordered timeline, and groups incidents from `ERROR` until recovery with `INFO`.

## Scope
- Parse log lines in the format `YYYY-MM-DD HH:MM:SS LEVEL MESSAGE`
- Expose `/timeline` and `/incidents` API endpoints
- Add tests, Docker, CI/CD, Puppet, and monitoring

## Milestones
1. Build parser module
2. Build timeline and incident logic
3. Create Flask API
4. Add unit and integration tests
5. Add Docker and docker-compose
6. Add GitHub Actions pipeline
7. Add Puppet and monitoring files
8. Final review and documentation

## Deliverables
- Working Flask API
- Sample log file
- Automated tests
- Docker setup
- CI pipeline
- Puppet manifest
- Monitoring scripts
- Course documentation
