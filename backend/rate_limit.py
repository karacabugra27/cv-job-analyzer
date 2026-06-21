from fastapi import Depends, HTTPException, status
from redis.asyncio import Redis

from backend.auth import CurrentUser, get_current_user
from backend.redis_client import get_redis

DAILY_LIMIT = 3
MINUTE_LIMIT = 1
DAY_TTL_SECONDS = 24 * 60 * 60
MINUTE_TTL_SECONDS = 60


def _fmt_remaining(seconds: int) -> str:
    if seconds <= 60:
        return f"{seconds} saniye"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} dakika"
    hours = minutes // 60
    return f"{hours} saat"


async def enforce_rate_limit(
    user: CurrentUser = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
) -> CurrentUser:
    day_key = f"rl:day:{user.id}"
    minute_key = f"rl:min:{user.id}"

    day_current_raw = await redis.get(day_key)
    day_current = int(day_current_raw) if day_current_raw is not None else 0
    if day_current >= DAILY_LIMIT:
        ttl = await redis.ttl(day_key)
        ttl = max(ttl, 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Günlük {DAILY_LIMIT} analiz hakkın doldu. {_fmt_remaining(ttl)} sonra tekrar dene.",
            headers={"Retry-After": str(ttl)},
        )

    minute_count = await redis.incr(minute_key)
    if minute_count == 1:
        await redis.expire(minute_key, MINUTE_TTL_SECONDS)

    if minute_count > MINUTE_LIMIT:
        ttl = await redis.ttl(minute_key)
        ttl = max(ttl, 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Dakikada {MINUTE_LIMIT} analiz hakkın var. Lütfen {_fmt_remaining(ttl)} bekle.",
            headers={"Retry-After": str(ttl)},
        )

    day_count = await redis.incr(day_key)
    if day_count == 1:
        await redis.expire(day_key, DAY_TTL_SECONDS)

    if day_count > DAILY_LIMIT:
        ttl = await redis.ttl(day_key)
        ttl = max(ttl, 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Günlük {DAILY_LIMIT} analiz hakkın doldu. {_fmt_remaining(ttl)} sonra tekrar dene.",
            headers={"Retry-After": str(ttl)},
        )

    return user
