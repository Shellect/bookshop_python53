from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings
from app.services.session_service import SessionService


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, session_service: SessionService):
        super().__init__(app)
        self.session_service = session_service


    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")
        is_authenticated = False
        if session_id:
            # Проверяем сессию - быстрая операция redis
            user_id = await self.session_service.resolve(session_id)
            if user_id:
                is_authenticated = True
                # Передаем ID пользователя в обработчик запроса
                request.state.user_id = user_id

        request.state.is_authenticated = is_authenticated
        response = await call_next(request)

        if getattr(request.state, "clear_session", False):
            response.delete_cookie("session_id", path="/")
            return response

        # Если сессия была изменена в процессе запроса
        if hasattr(request.state, "new_session_id"):
            response.set_cookie(

                key="session_id",
                value= session_id if is_authenticated and session_id else request.state.new_session_id,
                httponly=True,
                secure = not settings.debug,
                samesite = "lax",
                path = "/",
                max_age= self.session_service.timeout
            )

        return response