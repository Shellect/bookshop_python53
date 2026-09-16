from fastapi import APIRouter, Depends

from app.dependencies.services import get_cart_service
from app.services import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("")
async def get_cart(cart_service: CartService = Depends(get_cart_service)):
    return cart_service