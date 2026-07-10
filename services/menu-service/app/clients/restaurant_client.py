import logging
import httpx
from starlette import status
from app.exceptions.all_exceptions import RestaurantNotFound, ForbiddenException, RestaurantServiceUnavailableException, RequestTimeoutException
from app.core.config import settings
from uuid import UUID
from app.schemas.internal import RestaurantResponse
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log
from app.core.logger import logger


#HTTPX is a modern, fully-featured HTTP client for Python that FastAPI uses (and recommends) for making HTTP requests

class RestaurantClient:

    def __init__(self):
        self.base_url= settings.RESTAURANT_SERVICE_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=5.0)


    @retry(stop=stop_after_attempt(5), wait=wait_fixed(6), retry=retry_if_exception_type((RestaurantServiceUnavailableException,RequestTimeoutException, RestaurantNotFound)), before_sleep=before_sleep_log(logger, logging.WARNING), reraise=True)
    async def get_restaurant(self,restaurant_id: UUID):
        response = await self.client.get(f"/internal/restaurants/{restaurant_id}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise RestaurantNotFound(restaurant_id)
            if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
                raise ForbiddenException()
            if e.response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                raise RestaurantServiceUnavailableException()
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                raise RequestTimeoutException()
        restaurant = RestaurantResponse.model_validate(response.json())  ##respone.json() converts {"id":"...","owner_id":"...","status":"OPEN"} into python dict
        return restaurant


