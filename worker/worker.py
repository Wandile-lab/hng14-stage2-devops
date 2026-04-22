import redis
import time
import os
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Redis factory (no global connection)
def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379))
    )


# Job processor
def process_job(r, job_id):
    try:
        logger.info(f"Processing job {job_id}")

        r.hset(f"job:{job_id}", "status", "processing")

        time.sleep(2)  # simulate work

        r.hset(f"job:{job_id}", "status", "completed")

        logger.info(f"Done: {job_id}")

    except Exception as e:
        logger.error(f"Job failed: {job_id}, error: {e}")

        try:
            r.hset(f"job:{job_id}", "status", "failed")
        except Exception:
            logger.error("Failed to update job status due to Redis issue")


# Worker loop (recovery logic)
while True:
    try:
        r = get_redis()
        job = r.brpop("job", timeout=5)

        if job:
            _, job_id = job
            process_job(r, job_id.decode())

    except redis.exceptions.ConnectionError:
        logger.error("Redis lost. Retrying in 2s...")
        time.sleep(2)
