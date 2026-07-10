from pydantic import BaseModel, ConfigDict, Field
import uuid
from datetime import datetime
from decimal import Decimal

class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    is_available: bool = True
    is_featured: bool = False
    is_vegetarian: bool = False
    preparation_time: int = Field(default=20, ge=1)

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    is_available: bool | None = None
    is_featured: bool | None = None
    is_vegetarian: bool | None = None
    preparation_time: int | None = Field(default=None, ge=1)


class MenuItemResponse(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    restaurant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
