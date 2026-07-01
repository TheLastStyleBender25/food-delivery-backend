from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole
from uuid import UUID


class CreateUser(BaseModel):
    name : str
    email: EmailStr
    password: str
    role : UserRole

class UserResponse(BaseModel):
    id : UUID
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}