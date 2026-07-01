from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from app.core.config import settings
from app.core.redis_com import redis_client
from app.dependencies.roles import required_role
from app.models.enums import UserRole
from app.core.rate_limiter import rate_limit
from app.dependencies.database import get_db
from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.exceptions.auth_exceptions import EmailAlreadyExistsException, InvalidCredentialsException, InvalidRefreshTokenException
from app.dependencies.auth import get_current_user
from app.tasks.email_tasks import send_welcome_email
from app.schemas.password import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ping")
def ping():
    return {"ping": "pong"}

@router.post("/register", response_model=UserResponse)
def register(register_request:RegisterRequest, checker:None  = Depends(rate_limit(2, 60)), db: Session = Depends(get_db)):
    return AuthService.register_user(db, register_request)

@router.post("/login", response_model=TokenResponse)
def login(login_request:LoginRequest, checker:None  = Depends(rate_limit(2, 60)), db: Session = Depends(get_db)):
    return AuthService.login_user(db, login_request)

@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: RefreshTokenRequest, checker:None  = Depends(rate_limit(2, 60)), db: Session = Depends(get_db)):
    return AuthService.refresh_tokens(db, refresh_token)


@router.post("/logout")
def logout(refresh_token : RefreshTokenRequest,checker:None  = Depends(rate_limit(2, 60)), db: Session = Depends(get_db)):
    return AuthService.logout_user(db, refresh_token)


@router.get("/me", response_model=UserResponse)
def me(checker:None  = Depends(rate_limit(2, 60)), current = Depends(get_current_user)):
    return current


@router.get("/admin")
def admin_route(checker:None  = Depends(rate_limit(2, 60)), current_user = Depends(required_role(UserRole.ADMIN))):
    return {"message": "Hello Admin"}


@router.get("/customer")
def customer_route(checker:None  = Depends(rate_limit(2, 60)), current_user = Depends(required_role(UserRole.CUSTOMER))):
    return {"message": "Hello Customer"}

@router.get("/redis-test")
def redis_test(checker:None  = Depends(rate_limit(2, 60))):
    redis_client.set("hello", "world")
    return { "message": redis_client.get("hello") }


@router.get("/test-task")
def test_task():
    send_welcome_email.delay("test@example.com")
    return {"message": "Task queued"}

#since the token is not present inside the get and only inside the method its a query paramter
#if you want to change it into path paramter needs to add this @router.get("/verify-email/{token}") rest will be same
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db), checker:None  = Depends(rate_limit(2, 60))):
    return AuthService.verify_email(db, token)

@router.post("/forgot-password")
def request_forgot_password(request : ForgotPasswordRequest, db: Session = Depends(get_db), checker:None  = Depends(rate_limit(2, 60))):
    return  AuthService.forgot_password(db, request.email)


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db), checker:None  = Depends(rate_limit(2, 60))):
    return AuthService.reset_password(db,request)

@router.get("/test")
def login(checker:None  = Depends(rate_limit(2, 60))):
    return {"message": "Hello World"}