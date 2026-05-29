import redis.asyncio as aioredis
from config.settings import settings

_redis = None

async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

class RedisSessionStore:
    async def set(self, key: str, value: str, ttl: int = 3600):
        r = await get_redis()
        await r.setex(key, ttl, value)

    async def get(self, key: str) -> str | None:
        r = await get_redis()
        return await r.get(key)

    async def delete(self, key: str):
        r = await get_redis()
        await r.delete(key)
