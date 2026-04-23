from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import time

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


def get_redis_client():
    for _ in range(5):
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            client.ping()
            return client
        except redis.exceptions.ConnectionError:
            time.sleep(1)

    raise Exception("Redis unavailable after retries")


r = get_redis_client()


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())

    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", mapping={
        "status": "queued",
        "created_at": str(time.time())
    })

    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = r.hgetall(f"job:{job_id}")

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job.get("status")
    }
