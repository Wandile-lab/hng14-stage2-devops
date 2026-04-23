# hng14-stage2-devops
# Job Processing System

A containerised microservices application consisting of a Node.js frontend,
a Python/FastAPI backend, a Python worker, and Redis.

## Prerequisites

- Docker >= 24
- Docker Compose >= 2 (or `docker-compose` v1)
- Git

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/hng14-stage2-devops
cd hng14-stage2-devops

cp .env.example .env   # edit values if needed

docker-compose up --build
```

## Successful Startup

All four services should show as `healthy`:

NAME                              STATUS
redis                             healthy
hng14-stage2-devops_api_1         healthy
hng14-stage2-devops_worker_1      healthy
hng14-stage2-devops_frontend_1    healthy

Open http://localhost:3000 in your browser.

## Services

| Service  | Port | Description                  |
|----------|------|------------------------------|
| frontend | 3000 | Job submission UI            |
| api      | 8000 | FastAPI — internal only      |
| worker   | —    | Processes jobs from Redis    |
| redis    | —    | Queue — internal only        |

## Running Tests

```bash
cd api
pip install -r requirements.txt pytest pytest-cov
pytest tests/ --cov=. --cov-report=term
```

## CI/CD Pipeline

Stages run in order: lint → test → build → security scan → integration test → deploy

The deploy stage only runs on pushes to `main` and performs a rolling update
via SSH. Set the following secrets in GitHub Actions:
- `SERVER_HOST`
- `SERVER_USER`  
- `SERVER_SSH_KEY`
