from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.menu_item import MenuItem
from app.repositories.menu_item_Repository import MenuItemRepository
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.schemas.token_payload import TokenPayload
from app.exceptions.all_exceptions import NonCustomerException, MenuItemNotFoundException, NonRestaurantOwner, ForbiddenException
from app.clients.restaurant_client import RestaurantClient
from app.core.redis_component import redis_client
import json
from app.services.file_storage_service import FileStorageService
from app.schemas.internal import InternalMenuItemResponse



class MenuService:

    def __init__(self):
        self.repo = MenuItemRepository()
        self.restaurant_client = RestaurantClient()
        self.file_storage = FileStorageService()

    async def create_menu_item(self, db : AsyncSession, restaurant_id: UUID, data : MenuItemCreate, current_user:TokenPayload) -> MenuItemResponse:
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        restaurant = await self.restaurant_client.get_restaurant(restaurant_id)
        if restaurant.owner_id != current_user.sub:
            raise ForbiddenException()
        menu_item = MenuItem(
            restaurant_id=restaurant_id,
            name=data.name,
            description=data.description,
            price=data.price,
            is_available=data.is_available,
            is_featured=data.is_featured,
            is_vegetarian=data.is_vegetarian,
            preparation_time=data.preparation_time,
        )
        menu_item = await self.repo.create(db, menu_item)
        await db.commit()
        return menu_item

    async def get_menu_item(self,db: AsyncSession,menu_item_id: UUID, current_user:TokenPayload) -> MenuItemResponse | None:
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        cache_key = f"menu_item:{menu_item_id}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return MenuItemResponse.model_validate_json(cache_data)
        menu_item = await self.repo.get_by_id(db, menu_item_id)
        response = MenuItemResponse.model_validate(menu_item)
        await redis_client.setex(cache_key, 300, response.model_dump_json())
        return menu_item

    async def get_menu_items_by_restaurant(self,db: AsyncSession,restaurant_id: UUID, current_user:TokenPayload, page, page_size) -> list[MenuItemResponse]:
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        cache_key = f"menu_items_by_restaurant:{restaurant_id}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return [MenuItemResponse.model_validate(r) for r in json.loads(cache_data)]
        items = await self.repo.get_by_restaurant(db, restaurant_id)
        response = [MenuItemResponse.model_validate(r) for r in items]
        start = (page-1) & page_size
        end = start * page_size
        pagination = response[start:end]
        cache_value = json.dumps([json.loads(r.model_dump_json()) for r in pagination])
        await redis_client.setex(cache_key, 300, cache_value)
        return items

    async def update_menu_item(self,db: AsyncSession,menu_item_id: UUID,data: MenuItemUpdate, current_user:TokenPayload) -> MenuItemResponse:
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        menu_item = await self.repo.get_by_id(db=db,obj_id=menu_item_id)

        if menu_item is None:
            raise MenuItemNotFoundException()

        if data.name is not None:
            menu_item.name = data.name

        if data.description is not None:
            menu_item.description = data.description

        if data.price is not None:
            menu_item.price = data.price

        if data.is_available is not None:
            menu_item.is_available = data.is_available

        if data.is_featured is not None:
            menu_item.is_featured = data.is_featured

        if data.is_vegetarian is not None:
            menu_item.is_vegetarian = data.is_vegetarian

        if data.preparation_time is not None:
            menu_item.preparation_time = data.preparation_time

        await db.commit()
        await db.refresh(menu_item)
        return menu_item


    async def delete_menu_item(self,db: AsyncSession,menu_item_id: UUID, current_user:TokenPayload) -> None:
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        menu_item = await self.repo.get_by_id(db,menu_item_id)
        if menu_item is None:
            raise MenuItemNotFoundException()
        await self.repo.delete(db,menu_item)
        await db.commit()

    async def get_available_menu_items(self,db: AsyncSession,restaurant_id: UUID, current_user:TokenPayload, page, page_size):
        self.checker_for_user(current_user.role, "CUSTOMER")
        cache_key = f"available_items:{restaurant_id}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return [MenuItemResponse.model_validate_json(c) for c in json.loads(cache_data)]
        items = await self.repo.get_available_items(db,restaurant_id)
        response = [MenuItemResponse.model_validate(r) for r in items]
        start = (page -1) * page_size
        end = start + page_size
        pagination = response[start:end]
        cache_value = json.dumps([json.loads(r.model_dump_json()) for r in pagination])
        await redis_client.setex(cache_key, 300, cache_value)
        return items


    async def upload_menu_image(self, db:AsyncSession, menu_id:UUID, image:UploadFile, current_user:TokenPayload):
        self.checker_for_user(current_user.role, "RESTAURANT_OWNER")
        menu_item = await self.repo.get_by_id(db,menu_id)
        if menu_item is None:
            raise MenuItemNotFoundException()
        if menu_item.image_url:
            await self.file_storage.delete_menu_image(menu_item.image_url)
        image_url = await self.file_storage.save_menu_image(image)
        menu_item.image_url = image_url

        await db.commit()
        await db.refresh(menu_item)

        return menu_item


    async def delete_menu_image(self, image_url: str):
        await self.file_storage.delete_menu_image(image_url)


    async def get_menu_item_internal(self, db:AsyncSession, menu_item_id:UUID):
        menu_item = await self.repo.get_by_id(db,menu_item_id)
        if menu_item is None:
            raise MenuItemNotFoundException()
        response = InternalMenuItemResponse.model_validate(menu_item)
        return response



    def checker_for_user(self, user, val):
        if user != val:
            if val == "CUSTOMER":
                raise NonCustomerException()
            elif val == "RESTAURANT_OWNER":
                raise NonRestaurantOwner()


