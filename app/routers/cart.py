from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.dependencies.services import ensure_session_id, get_cart_service
from app.schemas.cart import CartItemRequest, CartQtyRequest, CartItemResponse, CartResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


def _to_response(items: dict[str, int]) -> CartResponse:
    return CartResponse(
        items=[CartItemResponse(book_id=book_id, qty=qty) for book_id, qty in items.items()]
    )


def _identity(request: Request) -> tuple[str | None, str | None]:
    return getattr(request.state, "user_id", None), getattr(request.state, "session_id", None)


@router.get("", response_model=CartResponse)
async def get_cart(
    request: Request,
    cart_service: CartService = Depends(get_cart_service),
):
    user_id, session_id = _identity(request)
    return _to_response(await cart_service.get_items(user_id, session_id))


@router.post("/items", response_model=CartResponse)
async def add_cart_item(
    request: Request,
    body: CartItemRequest,
    cart_service: CartService = Depends(get_cart_service),
    session_id: str = Depends(ensure_session_id),
):
    user_id = getattr(request.state, "user_id", None)
    return _to_response(await cart_service.add(user_id, session_id, body.book_id, body.qty))


@router.patch("/items/{book_id}", response_model=CartResponse)
async def set_cart_item_qty(
    book_id: UUID,
    request: Request,
    body: CartQtyRequest,
    cart_service: CartService = Depends(get_cart_service),
    session_id: str = Depends(ensure_session_id),
):
    user_id = getattr(request.state, "user_id", None)
    return _to_response(await cart_service.set_qty(user_id, session_id, book_id, body.qty))


@router.delete("/items/{book_id}", response_model=CartResponse)
async def remove_cart_item(
    book_id: UUID,
    request: Request,
    cart_service: CartService = Depends(get_cart_service),
    session_id: str = Depends(ensure_session_id),
):
    user_id = getattr(request.state, "user_id", None)
    return _to_response(await cart_service.remove(user_id, session_id, book_id))


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    request: Request,
    cart_service: CartService = Depends(get_cart_service),
    session_id: str = Depends(ensure_session_id),
):
    user_id = getattr(request.state, "user_id", None)
    await cart_service.clear(user_id, session_id)
