from datetime import timedelta, datetime, UTC
from jose import jwt, JWTError
from app.core.config import settings
from app.exceptions.auth_exceptions import InvalidTokenException


def create_access_token(user_id:str, role:str):
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role ,"exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id:str):
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token:str):
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        raise InvalidTokenException()

def create_email_verification_token(user_id:str):
    expire = datetime.now(UTC) + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
    payload = {"sub":str(user_id), "type": "email_verification", "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)