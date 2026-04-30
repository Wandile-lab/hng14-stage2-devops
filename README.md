# Job Processing System
![CI](https://github.com/Wandile-lab/hng14-stage2-devops/actions/workflows/ci.yml/badge.svg?branch=main)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker\&logoColor=white)
![CI](https://github.com/Wandile-lab/hng14-stage2-devops/actions/workflows/ci.yml/badge.svg?branch=main)
![Security](https://img.shields.io/badge/Security-Trivy%20Scanned-brightgreen?logo=aquasecurity\&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Node](https://img.shields.io/badge/node-18-green)




A production-ready, containerized microservices system with a full CI/CD pipeline, built to simulate real-world DevOps responsibilities: reliability, scalability, and automated delivery.

## Architecture Overview

This system consists of four services:

- Frontend (Node.js) — User interface for submitting and tracking jobs
- API (FastAPI) — Handles job creation and status queries
- Worker (Python) — Processes jobs asynchronously
- Redis — Message broker between API and Worker

## Flow:

- User submits job → Frontend
- Frontend calls API
- API pushes job to Redis
- Worker consumes + processes job
- Status stored and retrieved via API

## Tech Stack
- Docker & Docker Compose
- Node.js (Frontend)
- Python + FastAPI (API)
- Python Worker
- Redis
- GitHub Actions (CI/CD)
- Trivy (Security Scanning)

## Prerequisites
- Docker ≥ 24
- Docker Compose ≥ 2
- Git

Verify installation:
```
docker --version
docker compose version
```

## Quick Start (From Scratch)
```
git clone https://github.com/Wandile-lab/hng14-stage2-devops.git
cd hng14-stage2-devops

cp .env.example .env

docker compose up --build
```

Expected Startup Behavior

All services must pass health checks before becoming available.

Check status:
```
docker compose ps
```

|NAME                           |   STATUS  |
|-------------------------------|-----------|
|redis                          |   healthy |
|hng14-stage2-devops_api_1      |   healthy |
|hng14-stage2-devops_worker_1   |   healthy |
|hng14-stage2-devops_frontend_1 |   healthy |

## Access app:
Open http://localhost:3000 in your browser.

## Services

| Service  | Port | Description                  |
|----------|------|------------------------------|
| frontend | 3000 | Job submission UI            |
| api      | 8000 | FastAPI — internal only      |
| worker   | —    | Processes jobs from Redis    |
| redis    | —    | Queue — internal only        |

## Configuration

- All configuration is handled via environment variables.

- See `.env.example` for required variables.

- ⚠️ No secrets are hardcoded or stored in images.

## Networking
- All services communicate over an internal Docker network
- Redis is NOT exposed externally
- API is internal-only (frontend is the public entry point)

## Running Tests

```bash
cd api
pip install -r requirements.txt pytest pytest-cov
pytest tests/ --cov=. --cov-report=term
```
- Redis is mocked
- Minimum 3 test cases
- Coverage report generated in CI

## Production Considerations Implemented
- Non-root containers
- Multi-stage builds (optimized images)
- Health checks for all services
- Resource limits (CPU & memory)
- Dependency-aware startup (wait for healthy services)

## CI/CD Pipeline
Pipeline runs on GitHub Actions (ubuntu-latest):

## Stages (strict order):
- Stages run in order: lint → test → build → security scan → integration test → deploy

### 1. Lint
- flake8 (Python)
- eslint (JS)
- hadolint (Dockerfiles)
### 2. Test
- pytest with coverage
- artifact uploaded
### 3. Build
- Images tagged with:
  - latest
  - Git SHA
- Pushed to local registry (service container)
### 4. Security Scan
- Trivy scan
- Fails on CRITICAL vulnerabilities
- SARIF report uploaded
### 5. Integration Test
- Full stack spun up
- Job submitted via frontend
- System polled until completion
- Stack torn down cleanly
### 6. Deploy (main branch only)
- Rolling update strategy:
- New container must pass health check
- Old container stopped only after success
- Timeout: 60 seconds
- Failure = rollback (old container stays)

## Failure Handling
- Any pipeline stage failure stops execution
- Health check failures block deployment
- Integration test ensures full system reliability

## Debugging Tips
- Check logs:
```
docker compose logs -f
```

## Restart services:
```
docker compose down
docker compose up --build
```
## Inspect containers:
```
docker inspect <container_id>
```

## Project Files
`README.md` → Setup & system overview
`FIXES.md` → All identified bugs + fixes (file, line, explanation)
`.env.example` → Required environment variables

## What This Project Demonstrates
- Real-world DevOps workflow
- Debugging broken systems
- Secure containerization practices
- CI/CD pipeline design
- System reliability under orchestration
  
## Notes
- No secrets stored in repo or images
- Redis is internal-only by design
- Designed to run entirely on local + GitHub free tier
