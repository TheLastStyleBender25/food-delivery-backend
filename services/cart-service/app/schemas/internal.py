from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID


class InternalMenuItemResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    price: Decimal
    is_available: bool


class InternalCartItemResponse(BaseModel):
    restaurant_id: UUID
    menu_item_id: UUID
    quantity: int
    price_at_addition: Decimal


class InternalCartResponse(BaseModel):
    items: list[InternalCartItemResponse]
    subtotal: Decimal