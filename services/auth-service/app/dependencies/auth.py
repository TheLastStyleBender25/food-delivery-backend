from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import json
from sqlalchemy.orm import Session
from app.core.cache import get_user_cache, set_user_cache
from app.core.jwt import decode_token
from app.core.logger import logger
from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse

security = HTTPBearer()

def get_current_user(credentials_request: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials_request.credentials
    try:
        payload = decode_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    cached_user = get_user_cache(user_id)
    if cached_user:
        logger.info(f"CACHE HIT: {user_id}")
        user_data = json.loads(cached_user)
        return UserResponse(id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
            created_at=user_data["created_at"])
    logger.info(f"CACHE MISS: {user_id}")
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat()
    }
    set_user_cache(user_id, user_data)
    return user
