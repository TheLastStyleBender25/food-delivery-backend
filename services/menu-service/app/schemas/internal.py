from uuid import UUID
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class RestaurantResponse(BaseModel):
    id: UUID
    owner_id: UUID
    status: str

class InternalMenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    restaurant_id: UUID
    name: str
    price: Decimal
    is_available: bool
