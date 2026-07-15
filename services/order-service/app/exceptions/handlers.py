from fastapi import  Request
from fastapi.responses import JSONResponse
from starlette import status
from app.core.logger import logger
from app.exceptions.all_exceptions import RateLimitExceededException, ForbiddenException, CannotCancelOrderException,\
    CartServiceUnavailableException, RequestTimeoutException, CartItemNotFoundException, CartNotFoundException, MenuItemNotFoundException, MenuServiceUnavailableException, OrderNotFoundException



async def RateLimitExceededExceptionHandler(request:Request, ex:RateLimitExceededException):
    logger.exception(f"Rate limit exceeded: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,content= "Rate limit exceeded")

async def CartItemNotFoundExceptionHandler(request:Request, ex:CartItemNotFoundException):
    logger.exception(f"Item is not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Item not found")

async def ForbiddenExceptionHandler(request:Request, ex:ForbiddenException):
    logger.exception(f"Not Allowed: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Not Allowed")

async def CartServiceUnavailableExceptionHandler(request:Request, ex:CartServiceUnavailableException):
    logger.exception(f"Service Unavailable: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,content= "Service Unavailable")

async def RequestTimeoutExceptionHandler(request:Request, ex:RequestTimeoutException):
    logger.exception(f"Request Timeout: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_408_REQUEST_TIMEOUT,content= "Request Timeout")


async def CartNotFoundExceptionHandler(request:Request, ex:CartNotFoundException):
    logger.exception(f"Not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Not found")

async def MenuItemNotFoundExceptionHandler(request:Request, ex:MenuItemNotFoundException):
    logger.exception(f"Item is not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Item not found")


async def MenuServiceUnavailableExceptionHandler(request:Request, ex:MenuServiceUnavailableException):
    logger.exception(f"Service Unavailable: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,content= "Service Unavailable")


async def MOrderNotFoundExceptionHandler(request:Request, ex:OrderNotFoundException):
    logger.exception(f"Not found: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= "Not found")

async def CannotCancelOrderExceptionHandler(request:Request, ex:CannotCancelOrderException):
    logger.exception(f"Cannot perform: {request.url}", exc_info=ex)
    return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,content= "Cannot perform")

