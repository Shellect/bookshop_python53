from redis.asyncio import Redis

from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.services import AuthService, SessionService, UserService

@lru_cache()
def get_redis_client() -> Redis:
    return Redis(
       host=settings.redis_host,
       port=settings.redis_port,
       db=settings.redis_db,
       password=settings.redis_password,
       decode_responses = True
    )

@lru_cache()
def get_session_service() -> SessionService:
    redis_client = get_redis_client()
    return SessionService(redis_client)


def get_user_service(
    database: AsyncSession = Depends(get_db)
) -> UserService:
    return UserService(database)


def get_auth_service(
    session_service: SessionService = Depends(get_session_service),
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(session_service, user_service)


