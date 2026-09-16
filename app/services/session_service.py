import json
import uuid

from datetime import datetime, timezone
from fastapi import Request
from typing import Optional

from app.core.redis import RedisManager


class SessionService:
    """
    Сервис для взаимодействия с Redis
    """

    def __init__(self, redis_manager: RedisManager):
        self.redis_manager = redis_manager
        self.timeout = 86400  # 24
        self.cookie_name = "session_id"

    def _session_key(self, session_id: str) -> str:
        return f"session:{session_id}"

    def _user_sessions_key(self, user_id: str) -> str:
        return f"user_session:{user_id}"

    async def create_session(
            self,
            user_id: Optional[str] = None,
            session_id: Optional[str] = None
        ) -> str:
        session_id = session_id or str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        session_data = {
            "user_id": str(user_id) if user_id else None,
            "created_at": now
        }
        redis_client = self.redis_manager.get_client()

        # Store session in redis with TTL
        await redis_client.setex(self._session_key(session_id), self.timeout, json.dumps(session_data))

        if user_id:
            # Store user session
            await redis_client.sadd(self._user_sessions_key(user_id), session_id)

        return session_id

    async def resolve(self, session_id: str) -> Optional[dict]:
        key = self._session_key(session_id)
        redis_client = self.redis_manager.get_client()

        # Load session from redis
        if user := await redis_client.get(key):
            await redis_client.expire(key, self.timeout)
            # Return user from session
            return json.loads(user)
        return None



    async def attach_user(self, session_id: str, user_id: str) -> str:
        key = self._session_key(session_id)
        redis_client = self.redis_manager.get_client()

        if raw := await redis_client.get(key):
            user = json.loads(raw)
            if (old_user_id := user.get("user_id")) and old_user_id != user_id:
                await redis_client.srem(self._user_sessions_key(old_user_id), session_id)
            user["user_id"] = user_id

            await redis_client.setex(key,  self.timeout, json.dumps(user))

        else:
            # Сессия уже истекла - создаем заново
            now = datetime.now(timezone.utc).isoformat()
            await redis_client.setex(key, self.timeout, json.dumps({
                "user_id": user_id,
                "created_at": now
            }))

        await redis_client.sadd(self._user_sessions_key(user_id), session_id)
        return session_id



    async def delete_session(self, session_id: str) -> None:
        key = self._session_key(session_id)
        redis_client = self.redis_manager.get_client()

        # Load data from session
        if (data := await redis_client.get(key)) and (
            user_id := json.loads(data).get("user_id")
        ):
            await redis_client.srem(self._user_sessions_key(user_id), session_id)
        await redis_client.delete(key)

    async def delete_user_sessions(self, user_id: str) -> None:
        user_key = self._user_sessions_key(user_id)
        redis_client = self.redis_manager.get_client()

        # Load all user session keys
        if session_ids := await redis_client.smembers(user_key):
            keys = [self._session_key(sid) for sid in session_ids]
            await redis_client.delete(*keys)
        await redis_client.delete(user_key)
