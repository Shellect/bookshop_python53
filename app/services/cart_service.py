from fastapi import Request

from app.core.redis import RedisManager
from app.services.session_service import SessionService

class CartService:

    def __init__(self, redis_manager: RedisManager, session_service: SessionService):
        self.redis_manager = redis_manager
        self.session_service = session_service


    def _cart_key(self, request: Request):
        if (user := getattr(request.state, "user")) and (user_id := user.get("user_id")):
            return "cart:user:" + user_id
        return "cart:session:" + request.cookies.get("session_id")

    async def create_cart(self):
        pass

