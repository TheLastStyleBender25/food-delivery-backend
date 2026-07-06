from fastapi import Request
from app.core.redis_component import redis_client
from app.exceptions.all_exceptions import RateLimitExceededException

def rate_limit(max:int, size:int):
    def dependency(request:Request):
        ip = request.client.host
        key = f"rate_limit:{request.url.path}:{ip}"
        cur = redis_client.incr(key)
        if cur == 1:
            redis_client.expire(key, size)
        if cur > max:
            raise RateLimitExceededException()
    return dependency
