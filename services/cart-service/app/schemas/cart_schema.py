from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class CartItemBase(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    menu_item_id: UUID


class CartItemUpdate(BaseModel):
    pass


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    restaurant_id: UUID
    menu_item_id: UUID
    quantity: int
    price_at_addition: Decimal
    created_at: datetime
    updated_at: datetime


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    subtotal: Decimal