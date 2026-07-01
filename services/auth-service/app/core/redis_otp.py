from app.core.config import settings
from app.core.redis_com import redis_client

def save_otp(email:str, otp:str):
    redis_client.set(f"reset_otp:{email}", otp, ex=settings.OTP_EXPIRATION_SECONDS)

def get_otp(email:str):
    return redis_client.get(f"reset_otp:{email}")

def delete_otp(email:str):
    redis_client.delete(f"reset_otp:{email}")