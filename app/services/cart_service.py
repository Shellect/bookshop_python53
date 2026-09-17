from uuid import UUID

from redis.asyncio import Redis

from app.core.config import settings


class CartService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.guest_ttl = settings.session_ttl_seconds
        self.user_ttl = settings.cart_user_ttl_seconds

    def _guest_key(self, session_id: str) -> str:
        return f"cart:session:{session_id}"

    def _user_key(self, user_id: str) -> str:
        return f"cart:user:{user_id}"

    def _cart_key(self, user_id: str | None, session_id: str | None) -> str | None:
        if user_id:
            return self._user_key(user_id)
        if session_id:
            return self._guest_key(session_id)
        return None

    def _ttl(self, user_id: str | None) -> int:
        return self.user_ttl if user_id else self.guest_ttl

    async def _touch(self, key: str, user_id: str | None) -> None:
        await self.redis.expire(key, self._ttl(user_id))

    async def get_items(
        self, user_id: str | None, session_id: str | None
    ) -> dict[str, int]:
        key = self._cart_key(user_id, session_id)
        if not key:
            return {}
        raw = await self.redis.hgetall(key)
        if not raw:
            return {}
        await self._touch(key, user_id)
        return {book_id: int(qty) for book_id, qty in raw.items()}

    async def add(
        self,
        user_id: str | None,
        session_id: str | None,
        book_id: UUID,
        qty: int,
    ) -> dict[str, int]:
        key = self._cart_key(user_id, session_id)
        if not key:
            return {}
        field = str(book_id)
        await self.redis.hincrby(key, field, qty)
        current = int(await self.redis.hget(key, field) or 0)
        if current <= 0:
            await self.redis.hdel(key, field)
        await self._touch(key, user_id)
        return await self.get_items(user_id, session_id)

    async def set_qty(
        self,
        user_id: str | None,
        session_id: str | None,
        book_id: UUID,
        qty: int,
    ) -> dict[str, int]:
        key = self._cart_key(user_id, session_id)
        if not key:
            return {}
        field = str(book_id)
        if qty <= 0:
            await self.redis.hdel(key, field)
        else:
            await self.redis.hset(key, field, qty)
        await self._touch(key, user_id)
        return await self.get_items(user_id, session_id)

    async def remove(
        self,
        user_id: str | None,
        session_id: str | None,
        book_id: UUID,
    ) -> dict[str, int]:
        return await self.set_qty(user_id, session_id, book_id, 0)

    async def clear(self, user_id: str | None, session_id: str | None) -> None:
        key = self._cart_key(user_id, session_id)
        if key:
            await self.redis.delete(key)

    async def delete_guest_cart(self, session_id: str) -> None:
        await self.redis.delete(self._guest_key(session_id))

    async def merge_guest_into_user(self, session_id: str, user_id: str) -> None:
        guest_key = self._guest_key(session_id)
        user_key = self._user_key(user_id)
        items = await self.redis.hgetall(guest_key)
        if items:
            pipe = self.redis.pipeline()
            for book_id, qty in items.items():
                pipe.hincrby(user_key, book_id, int(qty))
            pipe.expire(user_key, self.user_ttl)
            pipe.delete(guest_key)
            await pipe.execute()
        else:
            await self.redis.delete(guest_key)
