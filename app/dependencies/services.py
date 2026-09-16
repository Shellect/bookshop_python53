from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.core.database import SessionLocal
from app.core.redis import redis_manager
from app.services import AuthService, CartService, SessionService, UserService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_session_service() -> SessionService:
    return SessionService(redis_manager)


def get_user_service(database: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(database)


def get_auth_service(
    session_service: SessionService = Depends(get_session_service),
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(session_service, user_service)


def get_cart_service(
    session_service: SessionService = Depends(get_session_service),
) -> CartService:
    return CartService(session_service)
