from fastapi import  Request
from fastapi.responses import JSONResponse
from starlette import status
from app.core.logger import logger
from app.exceptions.all_exceptions import RestaurantNotFound, InvalidRestaurant, NonRestaurantOwner, NonCustomerException, RestaurantNotOpenException, RateLimitExceededException

async def RestaurantNotFoundHanler(request:Request, ex:RestaurantNotFound):
    logger.exception(f"Restaurant not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Restaurant not found")

async def InvalidRestaurantHanler(request:Request, ex:InvalidRestaurant):
    logger.exception(f"You do not own this restaurant: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "You do not own this restaurant")

async def NonRestaurantOwnerHanlder(request:Request, ex:NonRestaurantOwner):
    logger.exception(f"Only restaurant owners can create restaurants: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "Only restaurant owners can create restaurants")

async def NonCustomerExceptionHanler(request:Request, ex:NonCustomerException):
    logger.exception(f"You are not a customer: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "You are not a customer")

async def RestaurantNotOpenExceptionHandler(request:Request, ex:RestaurantNotOpenException):
    logger.exception(f"Restaurant is closed: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "Restaurant is closed")

async def RateLimitExceededExceptionHandler(request:Request, ex:RateLimitExceededException):
    logger.exception(f"Rate limit exceeded: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "Rate limit exceeded")
