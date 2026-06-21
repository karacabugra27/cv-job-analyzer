import hashlib
import json

from redis.asyncio import Redis

ANALYSIS_CACHE_TTL = 24 * 60 * 60


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:32]


def analysis_cache_key(cv_bytes: bytes, job_text: str) -> str:
    cv_hash = _hash(cv_bytes)
    jd_hash = _hash(job_text.strip().encode("utf-8"))
    return f"analysis:{cv_hash}:{jd_hash}"


async def get_cached_analysis(redis: Redis, key: str) -> dict | None:
    raw = await redis.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


async def set_cached_analysis(redis: Redis, key: str, value: dict) -> None:
    await redis.set(key, json.dumps(value, ensure_ascii=False), ex=ANALYSIS_CACHE_TTL)
