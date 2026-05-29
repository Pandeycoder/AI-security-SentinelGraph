from infrastructure.redis.redis_client import RedisSessionStore
import json

class AgentMemory:
    def __init__(self):
        self._store = RedisSessionStore()

    async def store(self, session_id: str, user_input: str, response: str):
        history = await self.recall(session_id) or "[]"
        entries = json.loads(history)
        entries.append({"user": user_input, "assistant": response})
        await self._store.set(f"agent_memory:{session_id}", json.dumps(entries[-10:]))

    async def recall(self, session_id: str) -> str | None:
        return await self._store.get(f"agent_memory:{session_id}")
