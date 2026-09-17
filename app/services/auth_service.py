from typing import Optional, Tuple

from pwdlib import PasswordHash

from app.models.user import User
from app.schemas.user import UserCreateRequest, UserLoginRequest
from app.services.exceptions import AuthenticationError
from .cart_service import CartService
from .session_service import SessionService
from .user_service import UserService

pwd_context = PasswordHash.recommended()


class AuthService:
    """
    Сценарии аутентификации: регистрация, логин, logout.
    Не зависит от FastAPI Request — cookie выставляет роутер/middleware.
    """

    def __init__(self, session_service: SessionService, user_service: UserService, cart_service: CartService ):
        self.session_service = session_service
        self.user_service = user_service
        self.cart_service = cart_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password) -> str:
        return pwd_context.hash(password)

    async def _bind_session(self, current_session_id: Optional[str], user_id: str) -> str:
        if current_session_id:
            session_id = await self.session_service.attach_user(current_session_id, user_id)
            await self.cart_service.merge_guest_into_user(session_id, user_id)
            return session_id
        return await self.session_service.create_session(user_id)

    async def create_user(self, user_data: UserCreateRequest, current_session_id: Optional[str]) -> Tuple[User, str]:
        hashed_password = self.hash_password(user_data.password)
        user = await self.user_service.create(user_data, hashed_password)
        session_id = await self._bind_session(current_session_id, str(user.id))
        return user, session_id

    async def authenticate_user(self, user_data: UserLoginRequest, current_session_id: Optional[str]) -> Tuple[User, str]:
        user = await self.user_service.get_by_name(user_data.login)
        if not user or not user.is_active or not self.verify_password(user_data.password, user.hashed_password):
            raise AuthenticationError("Incorrect login or password")

        await self.user_service.update_last_login(user)
        session_id = await self._bind_session(current_session_id, str(user.id))
        return user, session_id

    async def logout(self, session_id: Optional[str]) -> None:
        if session_id:
            await self.session_service.delete_session(session_id)
            await self.cart_service.delete_guest_cart(session_id)

    async def logout_all(self, user: User) -> None:
        await self.session_service.delete_user_sessions(str(user.id))
