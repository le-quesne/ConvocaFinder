import time
from fastapi import Request, HTTPException, status
import redis
from redis.exceptions import RedisError

from .config import get_settings

settings = get_settings()
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate:{client_ip}:{request.url.path}"
    try:
        current = redis_client.get(key)
        if current and int(current) >= settings.rate_limit_per_minute:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Demasiadas solicitudes")
        pipe = redis_client.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, 60)
        pipe.execute()
    except RedisError:  # pragma: no cover - fallback
        return
