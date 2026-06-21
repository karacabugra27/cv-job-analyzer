import os

import redis.asyncio as redis

REDIS_URL = os.environ["REDIS_URL"]

redis_client: redis.Redis = redis.from_url(
    REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis() -> redis.Redis:
    return redis_client
