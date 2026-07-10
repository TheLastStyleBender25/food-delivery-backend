from fastapi import  Request
from fastapi.responses import JSONResponse
from starlette import status
from app.core.logger import logger
from app.exceptions.all_exceptions import RestaurantNotFound, InvalidRestaurant, NonRestaurantOwner, \
    NonCustomerException, RateLimitExceededException, MenuItemNotFoundException, ForbiddenException, \
    RestaurantServiceUnavailableException, RequestTimeoutException, InvalidImageExtensionException, InvalidImageTypeException, InvalidImageContentException, FileTooLargeException


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


async def RateLimitExceededExceptionHandler(request:Request, ex:RateLimitExceededException):
    logger.exception(f"Rate limit exceeded: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "Rate limit exceeded")

async def MenuItemNotFoundExceptionHandler(request:Request, ex:MenuItemNotFoundException):
    logger.exception(f"Item is not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Item not found")

async def ForbiddenExceptionHandler(request:Request, ex:ForbiddenException):
    logger.exception(f"Not Allowed: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Not Allowed")

async def RestaurantServiceUnavailableExceptionHandler(request:Request, ex:RestaurantServiceUnavailableException):
    logger.exception(f"Service Unavailable: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,content= "Service Unavailable")

async def RequestTimeoutExceptionHandler(request:Request, ex:RequestTimeoutException):
    logger.exception(f"Request Timeout: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_408_REQUEST_TIMEOUT,content= "Request Timeout")

async def InvalidImageExtensionExceptionHandler(request:Request, ex:InvalidImageExtensionException):
    logger.exception(f"Invalid imagee extension: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content= "invalid imagee extension")

async def InvalidImageTypeExceptionHandler(request:Request, ex:InvalidImageTypeException):
    logger.exception(f"Invalid image type: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content= "Invalid image type")

async def InvalidImageContentExceptionHandler(request:Request, ex:InvalidImageContentException):
    logger.exception(f"Invalid image content: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content= "Invalid image content")

async def FileTooLargeExceptionHandler(request:Request, ex:FileTooLargeException):
    logger.exception(f"File too large: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content= "File too large")

