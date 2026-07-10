from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.owner_menu_route import router as category_router
from app.api.v1.customer_menu_route import router as customer_router
from app.exceptions.all_exceptions import RestaurantNotFound, InvalidRestaurant, NonRestaurantOwner, NonCustomerException, RateLimitExceededException, MenuItemNotFoundException, ForbiddenException, RestaurantServiceUnavailableException, RequestTimeoutException, InvalidImageExtensionException, InvalidImageTypeException, InvalidImageContentException, FileTooLargeException
from app.exceptions.handlers import RestaurantNotFoundHanler, InvalidRestaurantHanler, NonRestaurantOwnerHanlder, NonCustomerExceptionHanler, RateLimitExceededExceptionHandler, MenuItemNotFoundExceptionHandler, ForbiddenExceptionHandler, RestaurantServiceUnavailableExceptionHandler, RequestTimeoutExceptionHandler, InvalidImageExtensionExceptionHandler, InvalidImageTypeExceptionHandler, InvalidImageContentExceptionHandler, FileTooLargeExceptionHandler


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_exception_handler(RestaurantNotFound, RestaurantNotFoundHanler)
app.add_exception_handler(InvalidRestaurant, InvalidRestaurantHanler)
app.add_exception_handler(NonRestaurantOwner, NonRestaurantOwnerHanlder)
app.add_exception_handler(NonCustomerException, NonCustomerExceptionHanler)
app.add_exception_handler(RateLimitExceededException, RateLimitExceededExceptionHandler)
app.add_exception_handler(RateLimitExceededException, RateLimitExceededExceptionHandler)
app.add_exception_handler(MenuItemNotFoundException, MenuItemNotFoundExceptionHandler)
app.add_exception_handler(ForbiddenException, ForbiddenExceptionHandler)
app.add_exception_handler(RequestTimeoutException, RequestTimeoutExceptionHandler)
app.add_exception_handler(RestaurantServiceUnavailableException, RestaurantServiceUnavailableExceptionHandler)
app.add_exception_handler(InvalidImageTypeException, InvalidImageTypeExceptionHandler)
app.add_exception_handler(InvalidImageExtensionException, InvalidImageExtensionExceptionHandler)
app.add_exception_handler(InvalidImageContentException, InvalidImageContentExceptionHandler)
app.add_exception_handler(FileTooLargeException, FileTooLargeExceptionHandler)


app.include_router(category_router)
app.include_router(customer_router)

# Mount a static file server at the "/uploads" URL path.
# This tells FastAPI to serve files from the local "uploads" folder
# directly over HTTP — no route handler needed.
#
# Example: a file saved at uploads/abc.png will be accessible at
#          http://yourserver.com/uploads/abc.png
#
# Arguments:
#   "/uploads"            → the URL prefix where files will be served
#   directory="uploads"   → the local folder on disk to serve files from
#   name="uploads"        → an internal name used to reference this mount
#                           (e.g. with request.url_for("uploads", path="abc.png"))

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")