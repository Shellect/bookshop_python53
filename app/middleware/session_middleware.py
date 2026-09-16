from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.services.session_service import SessionService


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, session_service: SessionService):
        super().__init__(app)
        self.session_service = session_service


    async def dispatch(self, request: Request, call_next):
        # Проверяем сессию - быстрая операция redis
        if (session_id := request.cookies.get("session_id")) and (user := await self.session_service.resolve(session_id)):  
            user_id = user.get("user_id")
            request.state.session_id = session_id
            request.state.user_id = user_id
            request.state.is_authenticated = user_id is not None
        else:
            new_session_id = await self.session_service.create_session()
            request.state.session_id = new_session_id
            request.state.user_id = None
            request.state.is_authenticated = False
            request.state.new_session_id = new_session_id

        response = await call_next(request)

        if getattr(request.state, "clear_session", False):
            response.delete_cookie("session_id", path="/")
            return response

        # Если сессия была изменена в процессе запроса
        if new_session_id := getattr(request.state, "new_session_id", False):
            response.set_cookie(
                key="session_id",
                value= new_session_id,
                httponly=True,
                secure = not settings.debug,
                samesite = "lax",
                path = "/",
                max_age= self.session_service.timeout
            )

        return response