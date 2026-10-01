from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.services import ensure_session_id, get_cart_service
from app.schemas.cart import CartItemRequest, CartResponse
from app.services.cart_service import GuestCartService, UserCartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(cart: GuestCartService | UserCartService = Depends(get_cart_service)):
    return await cart.get_items()

@router.put("/items", response_model=CartResponse, dependencies=[Depends(ensure_session_id)])
async def set_item(item: CartItemRequest, cart: GuestCartService | UserCartService = Depends(get_cart_service)):
    return await cart.set_item(item)


@router.delete("/items/{book_id}", response_model=CartResponse, dependencies=[Depends(ensure_session_id)])
async def remove_item(book_id: UUID, cart: GuestCartService | UserCartService = Depends(get_cart_service)):
    return await cart.remove(book_id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(ensure_session_id)])
async def clear_cart(cart: GuestCartService | UserCartService = Depends(get_cart_service)):
    await cart.clear()
