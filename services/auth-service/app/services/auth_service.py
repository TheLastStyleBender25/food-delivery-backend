from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logger import logger
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.core.security import hashed_password
from app.exceptions.auth_exceptions import EmailAlreadyExistsException, InvalidCredentialsException, InvalidRefreshTokenException, CeleryTaskException, UserNotFoundException, UserNotVerifiedException, IncorrectOTPException, InvalidTokenException
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from datetime import datetime, timedelta, UTC
from app.core.jwt import create_access_token, create_refresh_token, decode_token, create_email_verification_token
from app.core.security import verify_password, hash_token
from app.tasks import send_welcome_email, send_verification_email, send_reset_password_email
from app.core.otp import generate_otp
from app.core.redis_otp import save_otp, get_otp, delete_otp
from app.schemas.password import ResetPasswordRequest
#work
class AuthService:
    @staticmethod
    def register_user(db :Session, request :RegisterRequest):
        exist = UserRepository.get_by_email(db, email=request.email)
        if exist:
            raise EmailAlreadyExistsException()
        user = User(name=request.name, email=request.email,  password_hash=hashed_password(request.password), role=request.role)
        created_user = UserRepository.create(db, user=user)
        try:
            verification = create_email_verification_token(user.id)
            verification_link = (f"http://localhost:8000/auth/verify-email?token={verification}")
            send_verification_email.delay(request.email, verification_link)
        except Exception:
            raise CeleryTaskException()
            logger.error(f"Failed to send verification email: {e}")
        return created_user



    @staticmethod
    def login_user(db :Session, request :LoginRequest):
        user = UserRepository.get_by_email(db, email=request.email)
        if not user:
            raise UserNotFoundException()
        if not user.is_verified:
            raise UserNotVerifiedException()
        if not verify_password(request.password, user.password_hash):
            raise InvalidCredentialsException()
        RefreshTokenRepository.delete_by_id(db, user_id=user.id)

        access = create_access_token(str(user.id), user.role)
        refresh = create_refresh_token(str(user.id))

        rtkndb = RefreshToken(user_id=user.id, token_hash= hash_token(refresh), expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        RefreshTokenRepository.create(db, rtkndb)

        return TokenResponse(access_token=access, refresh_token=refresh)

    @staticmethod
    def refresh_tokens(db :Session, request :RefreshTokenRequest):
        incoming_hash = hash_token(request.refresh_token)
        record = RefreshTokenRepository.get_by_token_hash(db, token_hash=incoming_hash)
        if not record:
            raise InvalidRefreshTokenException()
        try:
            payload = decode_token(request.refresh_token)
        except Exception:
            raise InvalidRefreshTokenException()
        user_id = payload.get("sub")
        user = UserRepository.get_by_id(db, user_id=user_id)
        if not user:
            raise InvalidRefreshTokenException()
        RefreshTokenRepository.delete_by_id(db, user_id=user.id)
        access = create_access_token(str(user.id), user.role)
        refresh = create_refresh_token(str(user.id))
        rtkndb = RefreshToken(user_id=user.id, token_hash= hash_token(refresh), expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        RefreshTokenRepository.create(db, rtkndb)

        return TokenResponse(access_token=access, refresh_token=refresh)


    @staticmethod
    def logout_user(db :Session, request : RefreshTokenRequest):
        incoming_hash = hash_token(request.refresh_token)
        record = RefreshTokenRepository.get_by_token_hash(db, token_hash=incoming_hash)
        if not record:
            raise InvalidRefreshTokenException()
        try:
            payload = decode_token(request.refresh_token)
        except Exception:
            raise InvalidRefreshTokenException()
        user_id = payload.get("sub")
        user = UserRepository.get_by_id(db, user_id=user_id)
        if not user:
            raise InvalidRefreshTokenException()
        RefreshTokenRepository.delete_by_id(db, user_id=user.id)

        return {"message": "Logged out successful"}

    @staticmethod
    def verify_email(db :Session, token:str):
        try:
            payload = decode_token(token)
        except Exception:
            raise InvalidTokenException()
        user_id = payload.get("sub")
        user = UserRepository.get_by_id(db, user_id=user_id)
        if not user:
            raise UserNotFoundException()
        if user.is_verified:
            return {"message": "Email already verified"}
        user.is_verified = True
        db.commit()

        return {"message": "Email verified successfully"}


    @staticmethod
    def forgot_password(db: Session,email: str):
        user = UserRepository.get_by_email(db, email=email)
        if not user:
            raise UserNotFoundException()
        if not user.is_verified:
            raise UserNotVerifiedException()
        otp = generate_otp()
        save_otp(email, otp)
        try:
            send_reset_password_email.delay(email, otp)
        except Exception:
            raise CeleryTaskException()

        return {"message": "OTP sent successfully"}


    @staticmethod
    def reset_password(db: Session,request: ResetPasswordRequest):
        try:
            stored_otp = get_otp(email=request.email)
            print(f"otp is: {stored_otp}")
        except Exception:
            raise CeleryTaskException()
        if not stored_otp:
            raise IncorrectOTPException()
        if stored_otp != request.otp:
            raise IncorrectOTPException()
        user = UserRepository.get_by_email(db, email=request.email)
        if not user:
            raise UserNotFoundException()
        if not user.is_verified:
            raise UserNotVerifiedException()
        user.password_hash = hashed_password(request.new_password)
        db.commit()
        RefreshTokenRepository.delete_by_id(db, user_id=user.id)
        try:
            delete_otp(email=request.email)
        except Exception:
            raise CeleryTaskException()

        return {"message": "Password reset successfully"}




