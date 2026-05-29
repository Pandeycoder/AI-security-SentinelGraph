from infrastructure.redis.redis_client import RedisSessionStore
import json

class SessionMemory:
    def __init__(self):
        self._store = RedisSessionStore()

    async def save(self, session_id: str, data: dict, ttl: int = 3600):
        await self._store.set(f"session:{session_id}", json.dumps(data), ttl)

    async def load(self, session_id: str) -> dict | None:
        raw = await self._store.get(f"session:{session_id}")
        return json.loads(raw) if raw else None

    async def clear(self, session_id: str):
        await self._store.delete(f"session:{session_id}")
