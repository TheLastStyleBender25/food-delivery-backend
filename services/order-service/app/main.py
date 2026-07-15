from fastapi import FastAPI
from app.core.config import settings
from app.exceptions.all_exceptions import (
    RateLimitExceededException,
    CartItemNotFoundException,
    ForbiddenException,
    CartServiceUnavailableException,
    RequestTimeoutException,
    CartNotFoundException,
    MenuItemNotFoundException,
    MenuServiceUnavailableException,
)
from app.exceptions.handlers import (
    RateLimitExceededExceptionHandler,
    CartItemNotFoundExceptionHandler,
    ForbiddenExceptionHandler,
    CartServiceUnavailableExceptionHandler,
    RequestTimeoutExceptionHandler,
    CartNotFoundExceptionHandler,
    MenuItemNotFoundExceptionHandler,
    MenuServiceUnavailableExceptionHandler,
)
from app.api.v1.order_route import router as order_router


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_exception_handler(RateLimitExceededException, RateLimitExceededExceptionHandler)
app.add_exception_handler(CartItemNotFoundException, CartItemNotFoundExceptionHandler)
app.add_exception_handler(ForbiddenException, ForbiddenExceptionHandler)
app.add_exception_handler(CartServiceUnavailableException, CartServiceUnavailableExceptionHandler)
app.add_exception_handler(RequestTimeoutException, RequestTimeoutExceptionHandler)
app.add_exception_handler(CartNotFoundException, CartNotFoundExceptionHandler)
app.add_exception_handler(MenuItemNotFoundException, MenuItemNotFoundExceptionHandler)
app.add_exception_handler(MenuServiceUnavailableException, MenuServiceUnavailableExceptionHandler)

app.include_router(order_router)