import time
from collections import defaultdict
from fastapi import HTTPException

request_counts = defaultdict(list)

MAX_REQUESTS = 10
TIME_WINDOW = 60

def check_rate_limit(user_id: str):
    now = time.time()
    window_start = now - TIME_WINDOW

    request_counts[user_id] = [
        t for t in request_counts[user_id] if t > window_start
    ]

    if len(request_counts[user_id]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {MAX_REQUESTS} requests per minute."
        )

    request_counts[user_id].append(now)