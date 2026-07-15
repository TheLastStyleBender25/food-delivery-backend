from app.schemas.internal import InternalCartResponse
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log
from starlette import status
import httpx
from app.core.config import settings
from uuid import UUID
from app.core.logger import logger
from app.exceptions.all_exceptions import CartNotFoundException, CartServiceUnavailableException, RequestTimeoutException
import logging

class CartClient:

    def __init__(self):
        self.base_url = settings.CART_SERVICE_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=5.0)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(6), retry=retry_if_exception_type((CartNotFoundException, CartServiceUnavailableException)), before_sleep=before_sleep_log(logger=logger, log_level=logging.INFO), reraise=True)
    async def get_cart(self, customer_id: UUID):
        response = await self.client.get(f"/cart/internal/cart/{customer_id}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise CartNotFoundException()
            if e.response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                raise CartServiceUnavailableException()
        return InternalCartResponse.model_validate(response.json())


    @retry(stop=stop_after_attempt(5), wait=wait_fixed(6), retry=retry_if_exception_type((CartNotFoundException, CartServiceUnavailableException)), before_sleep=before_sleep_log(logger=logger, log_level=logging.INFO), reraise=True)
    async def clear_cart(self, customer_id: UUID):
        response = await self.client.delete(f"/cart/internal/cart/{customer_id}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise CartNotFoundException()
            if e.response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                raise CartServiceUnavailableException()
        return {"deleted"}