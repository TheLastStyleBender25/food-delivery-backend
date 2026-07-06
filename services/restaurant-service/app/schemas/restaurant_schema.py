from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.restaurant_status import RestaurantStatus
from datetime import time

class RestaurantCreate(BaseModel):
    name:str
    description:str
    phone:str
    address:str
    city:str
    state:str
    latitude:float
    longitude:float
    delivery_radius_km: float = 5
    minimum_order_amount: float = 0
    average_preparation_time_minutes: int = 20
    opens_at: time
    closes_at: time

class RestaurantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    latitude:float | None = None
    longitude:float | None = None
    delivery_radius_km: float | None = None
    minimum_order_amount: float | None = None
    average_preparation_time_minutes: int | None = None
    opens_at: time | None = None
    closes_at: time | None = None

class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:UUID
    owner_id:UUID
    name: str
    description: str
    phone: str
    address: str
    city: str
    state: str
    latitude: float
    longitude: float
    delivery_radius_km: float
    minimum_order_amount: float
    average_preparation_time_minutes: int
    opens_at: time
    closes_at: time


class RestaurantStatusUpdate(BaseModel):
    status : RestaurantStatus