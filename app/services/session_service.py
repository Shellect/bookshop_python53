import json
import uuid

from datetime import datetime, timezone
from redis.asyncio import Redis
from typing import Optional


class SessionService:
    """
    Сервис для взаимодействия с Redis
    """

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.timeout = 86400  # 24 часа

    def _session_key(self, session_id: str) -> str:
        return f"session:{session_id}"

    def _user_sessions_key(self, user_id: str) -> str:
        return f"user_session:{user_id}"

    async def create_session(self, user_id: str) -> str:
        """
        Store session in redis and returns sesion_id
        """
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        session_data = {
            "user_id": str(user_id),
            "created_at": now,
            "last_activity": now
        }

        # Store session in redis with TTL
        key = self._session_key(session_id)
        await self.redis_client.setex(key, self.timeout, json.dumps(session_data))

        # Store user session
        user_key = self._user_sessions_key(user_id)
        await self.redis_client.sadd(user_key, session_id)

        return session_id

    async def resolve(self, session_id: str) -> Optional[str]:
        key = self._session_key(session_id)
        data = await self.redis_client.get(key)
        if data:
            session_data = json.loads(data)
            await self.redis_client.expire(key, self.timeout)
            return session_data.get("user_id")
        return None

    async def delete_session(self, session_id: str) -> None:
        key = self._session_key(session_id)
        data = await self.redis_client.get(key)
        if data:
            user_id = json.loads(data).get("user_id")
            await self.redis_client.delete(key)
            if user_id:
                await self.redis_client.srem(self._user_sessions_key(user_id), session_id)
        else:
            await self.redis_client.delete(key)

    async def delete_user_sessions(self, user_id: str) -> None:
        user_key = self._user_sessions_key(user_id)
        session_ids = await self.redis_client.smembers(user_key)
        if session_ids:
            keys = [self._session_key(sid) for sid in session_ids]
            await self.redis_client.delete(*keys)
        await self.redis_client.delete(user_key)
