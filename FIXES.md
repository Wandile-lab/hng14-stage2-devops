
File: worker/worker.py
Line: ~15
Issue: Redis connection assumes localhost:6379 is always accessible, but fails when Redis runs in a container without port binding
Fix: Ensure Redis is exposed using `-p 6379:6379` OR make Redis host configurable via environment variable instead of hardcoding localhost

File: worker/worker.py
Issue: Worker attempts to connect to Redis immediately on startup. If Redis is not yet available, the worker crashes with a connection error and stops processing jobs.
Impact: The system becomes stuck with jobs permanentyl in "queued" state.
Fix: Implement retry logc Or ensure proper service dependency handling using health checks in Docker Compose.

File: api/main.py
Issue: Redis connection is hardcoded to localhost
Impact: Breaks in containerized environments and CI/CD pipelines
Fix: Replace with environment variable REDIS_HOST and add fallback configurations

File: api/main.py
Issue:No redis conncetion error handling or retry mechanism
Impact: API may fail silently or crash when redis is unavailable
Fix: Add try/except and connection validation with retry logic or startup health check

File: api/main.py
Issue: Missing proper HTTP error status codes for missing job
Impact:Clients recieve ambiguous 200 responses for failed lookups
Fix: Return HTTP 404 using FastAPI HTTPException

File: api/main.py
Issue: Job state model is incomplete(only "queued" exists)
Impact: No visibility into processing, failure, or completion states
Fix: Extend job lifecycle states: queued, processing,completed, failed

File: api/main.py
Issue:Redis connection was hardcoded to "localhost".
Impact:Breaks in containerized environments (Docker Compose, CI/CD) where services communicate via service names, not localhost.
Fix:Replaced hardcoded values with environment variables REDIS_HOST and REDIS_PORT using os.getenv().

File: api/main.py
Issue:No error handling for Redis connection failures.
Impact:API may crash or behave unpredictably when Redis is unavailable, leading to unreliable system behavior.
Fix:Implemented a retry mechanism with connection validation using client.ping() and retry attempts before failing.

File: api/main.py
Issue:API returned HTTP 200 even when a job was not found.
Impact:Clients cannot distinguish between successful and failed requests, breaking frontend logic and integration tests.
Fix:Replaced response with FastAPI HTTPException (404 status code).

File: api/main.py
Issue:Job lifecycle tracking was incomplete (only "queued" state existed).
Impact:No visibility into job processing stages, making debugging and system validation difficult.
Fix:Extended job metadata to include additional states (processing, completed, failed) and timestamps.

File: worker/worker.py
Issue:
Redis connection was hardcoded to "localhost".
Impact:Breaks in containerized and CI environments where Redis runs as a separate service.
Fix:Replaced with environment variables REDIS_HOST and REDIS_PORT.

File: worker/worker.py
Issue:Worker crashes if Redis is unavailable at startup or during execution.
Impact:Job processing halts completely, leaving jobs stuck in "queued" state.
Fix:Wrapped Redis operations in a retry loop with exception handling to allow recovery from connection failures.

File: worker/worker.py
Issue:No error handling during job processing.
Impact:Failures during job execution are not captured, and jobs may be incorrectly marked as completed.
Fix:Added try/except block in process_job() and introduced "failed" status for unsuccessful jobs.

File: worker/worker.py
Issue:Worker did not update job status during processing.
Impact:System lacks visibility into job lifecycle and progress.
Fix:Added "processing" state before execution begins.

File: worker/worker.py
Issue:Logging was implemented using print statements.
Impact:Logs lack structure, severity levels, and timestamps, making debugging difficult in production environments.
Fix:Replaced print statements with Python logging module using INFO level logging.

File: api/main.py
Issue:Redis port was incorrectly parsed from REDIS_HOST instead of REDIS_PORT, causing a ValueError when trying to convert "redis" to an integer.
Impact:API container crashed on startup, preventing the backend from running and breaking the entire system dependency chain.
Fix:Corrected environment variable usage

File: api/main.py
Issue:Redis client was initialized without proper retry resilience before usage.
Impact:System could fail during startup if Redis was not immediately ready, leading to unstable container orchestration.
Fix:Implemented retry-based Redis connection logic using ping() validation with fallback retries.

File: frontend/app.js
Issue:Frontend was using localhost:8000 to communicate with the API.
Impact:Docker containers could not resolve localhost correctly across services, causing frontend-to-backend communication failure.
Fix:Replaced with Docker service DNS name:
const API_URL = "http://api:8000";

File: docker-compose.yml
Issue:Frontend and API containers were failing due to host port conflicts and incorrect service communication assumptions.
Impact:Containers could not start reliably; system failed intermittently depending on host port availability.
Fix:
Ensured:
-Unique exposed ports (3000, 8000, 6379)
-Proper service-level networking using Docker internal DNS
-depends_on relationships between services

File: frontend/Dockerfile
Issue:Ownership assignment (chown) was applied after user switch logic could potentially conflict with file permissions.
Impact:Risk of permission-related container instability in stricter runtime environments.
Fix:
Ensured correct order:
Copy files first
Apply chown before switching to non-root user1

File: api/Dockerfile
Issue:Application dependencies were installed in builder stage but PATH was not properly exposed in runtime stage.
Impact:Risk of missing dependency execution in container runtime environment.
Fix:Explicitly set PATH:
ENV PATH=/home/appuser/.local/bin:$PATH

File: worker container
Issue:Worker health check relied on process detection (pgrep) which can be unreliable in containerized environments.
Impact:False unhealthy status reporting even when worker is running correctly.
Fix:Revised healthcheck strategy (process-based but acknowledged limitation). Future improvement: switch to Redis heartbeat or job polling metric.1~File: worker container

File: docker-compose logs system
Issue:Docker Compose CLI emitted internal KeyError: 'id' thread error during event streaming.
Impact:No functional impact, but noisy logs created confusion during debugging.
Fix:No application fix required — identified as Docker Compose CLI bug. Safe to ignore or upgrade Compose version.

# Bug Fixes

- **File:** `docker-compose.yml`
- **Line:** ~50 (frontend healthcheck)
- **Problem:** Healthcheck used `wget` which is not installed in the frontend image. The Dockerfile explicitly installs `curl` instead.
- **Fix:** Changed healthcheck to `curl -f http://localhost:3000/health`

## 
- **File:** `api/Dockerfile`
- **Line:** Final stage (after `FROM python:3.10-slim`)
- **Problem:** `curl` was not installed in the API image, but the HEALTHCHECK instruction calls `curl`. The health check would always fail, causing all dependent services to never start.
- **Fix:** Added `RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`

## 
- **File:** `docker-compose.yml`
- **Line:** `retries: 5` under `api` healthcheck
- **Problem:** Incorrect indentation (1 space instead of 6). Invalid YAML structure causes the field to be ignored or cause a parse error.
- **Fix:** Corrected indentation to align with `timeout` and `interval`

## 
- **File:** `worker/worker.py`
- **Line:** 4–9 (Redis connection at module level)
- **Problem:** Redis connection was made directly at startup with no retry logic. If Redis was not fully ready at the exact moment the worker started, the process would crash immediately and not recover.
- **Fix:** Wrapped connection in a retry loop (10 attempts, 1 second apart) matching the pattern used in `api/main.py`


Summary:

The application initially suffered from hardcoded configurations, lack of error handling, incomplete job lifecycle tracking, and weak logging practices.
These issues would cause failures in containerized and production environments.
All fixes were implemented to align the system with production-grade DevOps standards, ensuring resilience, observability, and environment portability.
