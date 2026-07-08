from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.restaurant_router import router as restaurant_router
from app.api.v1.internal_route import router as internal_router
from app.exceptions.all_exceptions import RestaurantNotFound, InvalidRestaurant, NonRestaurantOwner, NonCustomerException, RestaurantNotOpenException, RateLimitExceededException
from app.exceptions.handlers import RestaurantNotFoundHanler, InvalidRestaurantHanler, NonRestaurantOwnerHanlder, NonCustomerExceptionHanler, RestaurantNotOpenExceptionHandler, RateLimitExceededExceptionHandler


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_exception_handler(RestaurantNotFound, RestaurantNotFoundHanler)
app.add_exception_handler(InvalidRestaurant, InvalidRestaurantHanler)
app.add_exception_handler(NonRestaurantOwner, NonRestaurantOwnerHanlder)
app.add_exception_handler(NonCustomerException, NonCustomerExceptionHanler)
app.add_exception_handler(RestaurantNotOpenException, RestaurantNotOpenExceptionHandler)
app.add_exception_handler(RateLimitExceededException, RateLimitExceededExceptionHandler)

app.include_router(restaurant_router)
app.include_router(internal_router)


