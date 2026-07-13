from fastapi import Request
from app.core.redis_component import redis_client
from app.exceptions.all_exceptions import RateLimitExceededException

def rate_limit(max:int, window:int):
    async def dependency(request:Request):
        ip = request.client.host
        key = f"rate_limit:{request.url.path}:{ip}"
        cur = await redis_client.incr(key)
        if cur == 1:
            await redis_client.expire(key, window)
        if cur > max:
            raise RateLimitExceededException()
    return dependency