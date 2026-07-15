from app.schemas.internal import InternalMenuItemResponse
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log
from starlette import status
import httpx
from app.core.config import settings
from uuid import UUID
from app.core.logger import logger
from app.exceptions.all_exceptions import MenuItemNotFoundException, MenuServiceUnavailableException, RequestTimeoutException
import logging


class MenuClient:

    def __init__(self):
        self.base_url = settings.MENU_SERVICE_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=5.0)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(6), retry=retry_if_exception_type((MenuItemNotFoundException, MenuServiceUnavailableException)), before_sleep=before_sleep_log(logger=logger, log_level=logging.INFO), reraise=True)
    async def get_menu_item(self, menu_id:UUID):
        response = await self.client.get(f"/restaurants/internal/menu-items/{menu_id}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise MenuItemNotFoundException()
            if e.response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                raise MenuServiceUnavailableException()
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                raise RequestTimeoutException()
        menu_item = InternalMenuItemResponse.model_validate(response.json())
        return menu_item