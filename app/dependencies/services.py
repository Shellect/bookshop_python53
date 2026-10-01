from uuid import UUID

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.core.database import SessionLocal
from app.services import AuthService, SessionService, UserService
from app.services.cart_service import CartMergeService, GuestCartService, UserCartService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_session_service(request: Request) -> SessionService:
    return request.app.state.session_service


def get_user_service(database: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(database)


def get_cart_service(request: Request, db: AsyncSession = Depends(get_db)) -> UserCartService | GuestCartService:
    if user_id := getattr(request.state, "user_id", None):
        return UserCartService(db, UUID(user_id))
    return GuestCartService(request.app.state.redis, getattr(request.state, "session_id", None))


async def get_cart_merge_service(request: Request) -> AsyncGenerator[CartMergeService, None]:
    async with SessionLocal() as session:
        try:
            yield CartMergeService(request.app.state.redis, session)
        finally:
            await session.close()


def get_auth_service(
    session_service: SessionService = Depends(get_session_service),
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(session_service, user_service)


async def ensure_session_id(
    request: Request,
    session_service: SessionService = Depends(get_session_service),
) -> str:
    if session_id := getattr(request.state, "session_id", None):
        return session_id
    session_id = await session_service.create_session()
    request.state.session_id = session_id
    request.state.new_session_id = session_id
    return session_id
