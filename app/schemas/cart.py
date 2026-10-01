from uuid import UUID

from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):
    book_id: UUID
    qty: int = Field(..., ge=1, le=9)


class CartItemResponse(BaseModel):
    book_id: UUID
    qty: int


class CartResponse(BaseModel):
    items: list[CartItemResponse]
