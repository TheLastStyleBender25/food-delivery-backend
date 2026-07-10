from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.core.rate_limiter import rate_limit
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services.menu_service import MenuService
from app.schemas.token_payload import TokenPayload
from uuid import UUID

router = APIRouter(prefix="/restaurants", tags=["Customer Menu"])

service = MenuService()

@router.get("/{restaurant_id}/menu",response_model=list[MenuItemResponse])
async def get_restaurant_menu(restaurant_id: UUID, page:int = 1, page_size:int = 10, db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user),checker:None= Depends(rate_limit(2,60))):
    result = await service.get_available_menu_items(db,restaurant_id, current_user, page, page_size)
    return result