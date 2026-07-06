from pydantic import BaseModel
from uuid import UUID

class TokenPayload(BaseModel):
    sub:UUID
    role:str
    