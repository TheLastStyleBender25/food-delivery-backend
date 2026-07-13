from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID


class InternalMenuItemResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    price: Decimal
    is_available: bool