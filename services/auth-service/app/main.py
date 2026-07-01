from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.exceptions.handlers import email_exist_exception, invalid_credentials_exception, \
    invalid_refresh_token_exception, user_not_found_exception, rate_limit_exception, invalid_token_handler, celery_task_handler, incorrect_otp_handler, user_not_verified_handler
from app.exceptions.auth_exceptions import UserNotFoundException, InvalidCredentialsException, \
    InvalidRefreshTokenException, EmailAlreadyExistsException, RateLimitExceededException, UserNotVerifiedException, IncorrectOTPException, CeleryTaskException, InvalidTokenException

# Initialize the FastAPI application with a title
app = FastAPI(title="Auth-Service")

# ─── Rate Limiter Setup (must be configured before routers) ───────────────────


# Register a custom exception handler for RateLimitExceeded errors.
# When any route (including those from included routers) triggers a rate limit,
# FastAPI bubbles the exception up and this handler returns a proper 429 response.
app.add_exception_handler(RateLimitExceededException, rate_limit_exception)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception)
app.add_exception_handler(InvalidRefreshTokenException, invalid_refresh_token_exception)
app.add_exception_handler(UserNotFoundException, user_not_found_exception)
app.add_exception_handler(EmailAlreadyExistsException, email_exist_exception)
app.add_exception_handler(CeleryTaskException, celery_task_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
app.add_exception_handler(UserNotVerifiedException, user_not_verified_handler)
app.add_exception_handler(IncorrectOTPException, incorrect_otp_handler)

# ─── Router Registration (after middleware & state are fully configured) ───────

# Include the auth router — all routes defined inside auth_router will now
# be protected by SlowAPIMiddleware since it was registered above.
app.include_router(auth_router)

# ─── Root Endpoint ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    # Basic health-check / welcome endpoint
    return {"message": "Hello from auth service"}