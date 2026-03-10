import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import HTTPException, status


class InMemoryRateLimiter:
    def __init__(self):
        self._events: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str, limit: int, window_seconds: int, on_violation: Callable[[], None]) -> None:
        now = time.time()
        window_start = now - window_seconds
        bucket = self._events[key]
        while bucket and bucket[0] < window_start:
            bucket.popleft()
        if len(bucket) >= limit:
            on_violation()
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        bucket.append(now)
