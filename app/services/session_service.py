import json
import uuid

from datetime import datetime
from redis import Redis
from typing import Optional

from app.core.config import settings


class SessionService:
    """
    Сервис для взаимодействия с Redis
    """


    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.timeout = 86400 # 24 часа


    def create_session(self, user_id: int) -> str:
        """
        Store session in redis and returns sesion_id
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        session_data = {
            "user_id" : user_id,
            "created_at" : now,
            "last_activity": now
        }

        # Store session in redis with TTL
        key = f"session:{session_id}"
        self.redis_client.setex(key, self.timeout, json.dumps(session_data))

        # Store user session
        user_key = f"user_session:{user_id}"
        self.redis_client.sadd(user_key, session_id)
        self.redis_client.expire(user_key, self.timeout)

        return session_id


    def extend_session(self, session_id):
        key = f"session:{session_id}"
        self.redis_client.expire(session_id, self.timeout)


    def get_user(self, session_id: str) -> Optional[str]:
        key = f"session:{session_id}"
        data = self.redis.client.get(key)
        if data:
            session_data = json.loads(data)
            session_data["last_activity"] = datetime.utcnow().isoformat()
            self.redis_client.setex(key, 86400, json.dumps(session_data))
            return session_data.get("user")
        return None