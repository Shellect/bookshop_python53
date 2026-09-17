from contextlib import asynccontextmanager
from typing import Optional

from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings


class RedisManager:
    def __init__(self):
        self.pool: Optional[ConnectionPool] = None
        self.client: Optional[Redis] = None

    async def connect(self):
        self.pool = ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            max_connections=50,
            decode_responses=True,
        )
        self.client = Redis(connection_pool=self.pool)

    async def disconnect(self):
        if self.client:
            await self.client.aclose()
        if self.pool:
            await self.pool.disconnect()

    def get_client(self) -> Redis:
        if self.client is None:
            raise RuntimeError("Redis is not connected")
        return self.client


redis_manager = RedisManager()


@asynccontextmanager
async def lifespan(app):
    await redis_manager.connect()
    redis = redis_manager.get_client()
    app.state.redis = redis

    from app.services.session_service import SessionService

    app.state.session_service = SessionService(redis)
    yield
    await redis_manager.disconnect()
