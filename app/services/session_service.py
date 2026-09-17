import json
import uuid

from datetime import datetime, timezone
from typing import Optional

from redis.asyncio import Redis

from app.core.config import settings


class SessionService:
    """CRUD Redis-сессий. Не зависит от FastAPI Request."""

    def __init__(self, redis: Redis):
        self.redis = redis
        self.timeout = settings.session_ttl_seconds
        self.cookie_name = settings.session_cookie_name

    def _session_key(self, session_id: str) -> str:
        return f"session:{session_id}"

    def _user_sessions_key(self, user_id: str) -> str:
        return f"user_session:{user_id}"

    async def _index_user_session(self, user_id: str, session_id: str) -> None:
        key = self._user_sessions_key(user_id)
        await self.redis.sadd(key, session_id)
        await self.redis.expire(key, self.timeout)

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

        # Store session in redis with TTL
        await self.redis.setex(self._session_key(session_id), self.timeout, json.dumps(session_data))

        if user_id:
            # Store user session
            await self._index_user_session(str(user_id), session_id)

        return session_id

    async def resolve(self, session_id: str) -> Optional[dict]:
        key = self._session_key(session_id)

        # Load session from redis
        if raw := await self.redis.get(key):
            await self.redis.expire(key, self.timeout)
            data = json.loads(raw)
            if user_id := data.get("user_id"):
                await self.redis.expire(self._user_sessions_key(user_id), self.timeout)
            return data
        return None

    async def attach_user(self, session_id: str, user_id: str) -> str:
        key = self._session_key(session_id)

        if raw := await self.redis.get(key):
            user = json.loads(raw)
            if (old_user_id := user.get("user_id")) and old_user_id != user_id:
                await self.redis.srem(self._user_sessions_key(old_user_id), session_id)
            user["user_id"] = user_id
            await self.redis.setex(key, self.timeout, json.dumps(user))
        else:
            # Сессия уже истекла - создаем заново
            now = datetime.now(timezone.utc).isoformat()
            await self.redis.setex(key, self.timeout, json.dumps({
                "user_id": user_id,
                "created_at": now
            }))

        await self._index_user_session(user_id, session_id)
        return session_id

    async def delete_session(self, session_id: str) -> None:
        key = self._session_key(session_id)

        # Load data from session
        if (data := await self.redis.get(key)) and (
            user_id := json.loads(data).get("user_id")
        ):
            await self.redis.srem(self._user_sessions_key(user_id), session_id)
        await self.redis.delete(key)

    async def delete_user_sessions(self, user_id: str) -> None:
        user_key = self._user_sessions_key(user_id)

        # Load all user session keys
        if session_ids := await self.redis.smembers(user_key):
            keys = [self._session_key(sid) for sid in session_ids]
            await self.redis.delete(*keys)
        await self.redis.delete(user_key)
