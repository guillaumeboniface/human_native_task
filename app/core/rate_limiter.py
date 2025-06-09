from collections import deque
from fastapi import HTTPException, Request
from typing import Dict, Deque, Callable
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 180) -> None:
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, Deque[float]] = {}

    def is_rate_limited(self, client_id: str) -> bool:
        now = time.time()
        
        # Initialize the client's request queue if it doesn't exist
        if client_id not in self.requests:
            self.requests[client_id] = deque()
        
        # Remove requests older than 1 minute
        while self.requests[client_id] and now - self.requests[client_id][0] > 60:
            self.requests[client_id].popleft()
        
        # Check if the client has exceeded the rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return True
        
        # Add the current request timestamp
        self.requests[client_id].append(now)
        return False

# Create a global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next: Callable) -> None:
    client_id = request.headers.get("X-API-Key", request.client.host)
    
    if rate_limiter.is_rate_limited(client_id):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    return await call_next(request)