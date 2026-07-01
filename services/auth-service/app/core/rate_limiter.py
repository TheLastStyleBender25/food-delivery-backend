#from slowapi import Limiter
#from slowapi.util import get_remote_address
#limiter = Limiter(key_func=get_remote_address)
from alembic.command import current
from fastapi import HTTPException, Request
from app.core.redis_com import redis_client
from app.exceptions.auth_exceptions import RateLimitExceededException


def rate_limit(max_limit:int, window_size:int):
    def dependency(request: Request):
        ip = request.client.host
        key = f"rate_limit:{request.url.path}:{ip}"
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, window_size)
        if current > max_limit:
            raise RateLimitExceededException()
    return dependency

