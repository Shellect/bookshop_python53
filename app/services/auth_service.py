from datetime import datetime
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.user import UserLoginRequest, UserCreateRequest
from app.models.user import User
from .session_service import SessionService
from .user_service import UserService


class AuthService:
    """
    Сервис для аутентификации и управления пользователем
    """


    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, database: AsyncSession, session_service: SessionService, user_service: UserService):
        self.database = database
        self.session_service = session_service
        self.user_service = user_service


    def _create_session(self, request: Optional[Request], user_id: int):
        if request:
            session_id = self.session_service.create_session(user_id)
            request.state.new_session_id = session_id
            request.state.user_id = user_id
            request.state.is_authenticated = True


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def hash_password(self, password) -> str:
        pwd_context.hash(password)


    async def create_user(self, user_data: UserCreateRequest, request: Optional[Request] = None) -> User:
        hashed_password = self.hash_password(user_data.password)
        user = await self.user_service.create(user_data, hashed_password)
        self._create_session(request, user.id)
        return user


    async def authenticate_user(self, user_data: UserLoginRequest, request) -> Optional[User]:
        user = await self.user_service.get_by_name(user_data.login)
        if not user or not user.is_active or not self.verify_password(user_login_request.password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect login or password")

        user.last_login = datetime.utcnow()
        self.db.commit()

        self._create_session(request, user.id)

        return user

