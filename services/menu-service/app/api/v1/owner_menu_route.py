from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.core.rate_limiter import rate_limit
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services.menu_service import MenuService
from app.schemas.token_payload import TokenPayload
from uuid import UUID
from app.clients.restaurant_client import RestaurantClient


router = APIRouter(prefix="/owner", tags=["Owner Menu"])

service = MenuService()

@router.post("/restaurants/{restaurant_id}/menu-items",response_model=MenuItemResponse)
async def create_menu_item(restaurant_id: UUID,data: MenuItemCreate, db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    result = await service.create_menu_item(db, restaurant_id, data, current_user)
    return result

@router.get("/restaurants/{restaurant_id}/menu-items", response_model=list[MenuItemResponse])
async def get_menu_items(restaurant_id: UUID,page:int=1, page_size:int=10, db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    result = await service.get_menu_items_by_restaurant(db,restaurant_id, current_user, page, page_size)
    return result

@router.get("/menu-items/{menu_item_id}",response_model=MenuItemResponse)
async def get_menu_item(menu_item_id: UUID,db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    result = await service.get_menu_item(db,menu_item_id, current_user)
    return result

@router.put("/menu-items/{menu_item_id}",response_model=MenuItemResponse)
async def update_menu_item(menu_item_id: UUID,data: MenuItemUpdate,db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    result = await service.update_menu_item(db,menu_item_id,data, current_user)
    return result

@router.delete("/menu-items/{menu_item_id}")
async def delete_menu_item(menu_item_id: UUID,db: AsyncSession = Depends(get_db), current_user:TokenPayload=Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    await service.delete_menu_item(db,menu_item_id, current_user)
    return {"message": "Menu item deleted successfully"}

@router.put("/menu-items/{menu_item_id}/image")
async def upload_menu_image(menu_item_id: UUID, image: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
    result = await service.upload_menu_image(db,menu_item_id, image, current_user)
    return result


@router.get("/test-client/{restaurant_id}")
async def test_client(restaurant_id: UUID):
    restaurant_client = RestaurantClient()
    result = await restaurant_client.get_restaurant(restaurant_id)
    return result



