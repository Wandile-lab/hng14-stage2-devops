from fastapi import FastAPI
import redis
import uuid
import os
import time
from fastapi import HTTPException

app = FastAPI()

#Instead of hardcoding, Redis location is configurable
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  
REDIS_PORT = int(os.getenv("REDIS_HOST", 6379)) 

#Verifies dependency health
def get_redis_client():
    for i in range(5):  # retry 5 times
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            client.ping()  # forces connection check
            return client
        except redis.exceptions.ConnectionError:
            time.sleep(1)

    raise Exception("Redis is unavailable after retries")


r = get_redis_client()

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    r.hset(f"job:{job_id}", "created_at", str(time.time())) 
    return {"job_id": job_id}

#Return proper HTTP error codes
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": status.decode()}
