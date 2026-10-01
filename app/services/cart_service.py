from typing import Optional
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import Integer, column, delete, func, literal, select, values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert, UUID as PG_UUID

from app.core.config import settings
from app.models.book import Book
from app.models.cart import Cart
from app.schemas.cart import CartItemRequest, CartItemResponse, CartResponse
from app.services.exceptions import BookNotFoundError


class GuestCartService:
    """Гостевая корзина: Redis hash book_id -> qty, ключ привязан к session_id."""

    def __init__(self, redis: Redis, session_id: Optional[str]):
        self.redis = redis
        self.session_id = session_id

    def _cart_key(self) -> str:
        if self.session_id:
            return f"cart:session:{self.session_id}"
        raise RuntimeError("Guest cart requires session_id")

    async def get_items(self) -> CartResponse:
        items = []
        if self.session_id:
            key = self._cart_key()
            if raw := await self.redis.hgetall(key):
                await self.redis.expire(key, settings.cart_ttl)
                items = [CartItemResponse(book_id=book_id, qty=int(qty)) for book_id, qty in sorted(raw.items())]
        return CartResponse(items=items)

    async def set_item(self, item: CartItemRequest) -> CartResponse:
        await self.redis.hset(self._cart_key(), str(item.book_id), item.qty)
        return await self.get_items()

    async def remove(self, book_id: UUID) -> CartResponse:
        await self.redis.hdel(self._cart_key(), str(book_id))
        return await self.get_items()

    async def clear(self) -> None:
        await self.redis.delete(self._cart_key())


class UserCartService:
    """Корзина пользователя: строки таблицы cart, PK (user_id, book_id)."""

    def __init__(self, db: AsyncSession, user_id: UUID):
        self.db = db
        self.user_id = user_id

    async def get_items(self) -> CartResponse:
        stmt = select(Cart.book_id, Cart.quantity).where(Cart.user_id == self.user_id).order_by(Cart.book_id)
        raws = await self.db.execute(stmt)
        items = [CartItemResponse(book_id=book_id, qty=quantity) for book_id, quantity in raws]
        return CartResponse(items=items)

    async def set_item(self, item: CartItemRequest) -> CartResponse:
        source = select(
            literal(self.user_id, PG_UUID(as_uuid=True)),
            Book.id,
            literal(item.qty, Integer),
        ).where(Book.id == item.book_id)
        stmt = insert(Cart).from_select(["user_id", "book_id", "quantity"], source)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Cart.user_id, Cart.book_id],
            set_={
                "quantity": stmt.excluded.quantity,
                # onupdate модели в ON CONFLICT DO UPDATE не срабатывает, время задаём явно
                "updated_at": func.now()
            }
        )
        result = await self.db.execute(stmt)
        if result.rowcount == 0:
            await self.db.rollback()
            raise BookNotFoundError()
        await self.db.commit()
        return await self.get_items()

    async def remove(self, book_id: UUID) -> CartResponse:
        await self.db.execute(delete(Cart).where(Cart.user_id == self.user_id, Cart.book_id == book_id))
        await self.db.commit()
        return await self.get_items()
        
    async def clear(self) -> None:
        await self.db.execute(delete(Cart).where(Cart.user_id == self.user_id))
        await self.db.commit()

    async def add_many_existing(self, items: list[CartItemResponse]) -> None:
        """Вносит книги одним запросом. Книги вне каталога пропускаются."""

        if not items:
            return

        v = values(
            column("book_id", PG_UUID(as_uuid=True)),
            column("qty", Integer),
            name="v"
        ).data([(i.book_id, i.qty) for i in items])

        source = (
            select(literal(self.user_id, PG_UUID(as_uuid=True)), Book.id, v.c.qty)
            .select_from(v)
            .join(Book, Book.id == v.c.book_id)
            .where(v.c.qty > 0)
        )

        # Не обновляем корзину пользователя on conflict
        stmt = (
            insert(Cart)
            .from_select(["user_id", "book_id", "quantity"], source)
            .on_conflict_do_nothing(index_elements=[Cart.user_id, Cart.book_id])
        )

        await self.db.execute(stmt)
        await self.db.commit()


class CartMergeService:
    """Переносит гостевую корзину из Redis в корзину пользователя в Postgres."""

    def __init__(self, redis: Redis, db: AsyncSession):
        self.redis = redis
        self.db = db

    async def merge(self, session_id: str, user_id: UUID) -> None:
        guest_cart = GuestCartService(self.redis, session_id)
        cart = await guest_cart.get_items()
        await UserCartService(self.db, user_id).add_many_existing(cart.items)

        # Сюда доходим только после успешного commit
        await guest_cart.clear()
