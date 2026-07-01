from pydantic import BaseModel, EmailStr, Field
from app.models.enums import UserRole

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    role: UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

