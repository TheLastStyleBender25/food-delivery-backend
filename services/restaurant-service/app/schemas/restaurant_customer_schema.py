from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import time

class NearByRestaurantResponse(BaseModel):
    id : UUID
    name : str
    description : str
    minimum_order_amount: float
    average_preparation_time_minutes: int

class GetCustomerLocationRequest(BaseModel):
    latitude : float
    longitude : float

class CustomerRestaurantDetailResponse(BaseModel):
    id: UUID
    name: str
    description: str
    phone: str
    address: str
    minimum_order_amount: float
    average_preparation_time_minutes: int