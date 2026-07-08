from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.restaurant_status import RestaurantStatus

class InternalRestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:UUID
    owner_id:UUID
    status:RestaurantStatus

