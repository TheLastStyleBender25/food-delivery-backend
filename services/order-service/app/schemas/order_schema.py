from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.order_status import OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    menu_item_id: UUID
    name: str
    quantity: int
    price_at_order: Decimal
    created_at: datetime


class OrderBase(BaseModel):
    total_amount: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    restaurant_id: UUID
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class OrderDetailResponse(OrderResponse):
    items: list[OrderItemResponse]


class UpdateOrderStatus(BaseModel):
    status: OrderStatus

class CancelOrderResponse(BaseModel):
    message: str
