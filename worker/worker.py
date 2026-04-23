import time
import redis
import os

def get_redis():
    for _ in range(10):
        try:
            client = redis.Redis(
                host=os.getenv("REDIS_HOST", "redis"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True
            )
            client.ping()
            return client
        except redis.exceptions.ConnectionError:
            time.sleep(1)
    raise Exception("Redis unavailable after retries")

r = get_redis()

while True:
    job = r.rpop("jobs")

    if job:
        r.hset(f"job:{job}", "status", "processing")
        time.sleep(5)
        r.hset(f"job:{job}", "status", "completed")

    time.sleep(2)
