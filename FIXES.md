
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
0~Summary:

The application initially suffered from hardcoded configurations, lack of error handling, incomplete job lifecycle tracking, and weak logging practices.
These issues would cause failures in containerized and production environments.
All fixes were implemented to align the system with production-grade DevOps standards, ensuring resilience, observability, and environment portability.
