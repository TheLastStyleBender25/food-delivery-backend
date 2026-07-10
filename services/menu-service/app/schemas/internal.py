from uuid import UUID
from pydantic import BaseModel


class RestaurantResponse(BaseModel):
    id: UUID
    owner_id: UUID
    status: str