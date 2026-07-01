from fastapi import Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.models.enums import UserRole

def required_role(*allowed_roles):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=400, detail="Incorrect role supplied")
        return current_user
    return role_checker