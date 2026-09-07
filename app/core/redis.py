from contextlib import asynccontextmanager

from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings


class RedisManager:
    def __init__(self):
        self.pool: ConnectionPool = None
        self.client: Redis = None

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
        return self.client


redis_manager = RedisManager()


@asynccontextmanager
async def lifespan(app):
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()
