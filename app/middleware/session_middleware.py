from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cookie_name = settings.session_cookie_name
        incoming = request.cookies.get(cookie_name)
        session_service = request.app.state.session_service

        request.state.session_id = None
        request.state.user_id = None
        request.state.is_authenticated = False

        # Проверяем сессию - быстрая операция redis
        if incoming:
            if data := await session_service.resolve(incoming):
                user_id = data.get("user_id")
                request.state.session_id = incoming
                request.state.user_id = user_id
                request.state.is_authenticated = user_id is not None

        response = await call_next(request)

        # Logout
        if getattr(request.state, "clear_session", False):
            response.delete_cookie(cookie_name, path="/")
            return response

        # Если сессия была изменена в процессе запроса
        session_id = getattr(request.state, "new_session_id", None) or request.state.session_id
        if session_id:
            response.set_cookie(
                key=settings.session_cookie_name,
                value=session_id,
                httponly=True,
                secure=not settings.debug,
                samesite="lax",
                path="/",
                max_age=settings.session_ttl_seconds,
            )
        elif incoming:
            response.delete_cookie(cookie_name, path="/")

        return response
