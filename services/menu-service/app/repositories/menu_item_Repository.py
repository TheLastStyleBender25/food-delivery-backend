from select import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.menu_item import MenuItem
from uuid import UUID
from sqlalchemy import select


class MenuItemRepository(BaseRepository[MenuItem]):
    def __init__(self):
        super().__init__(MenuItem)


    async def get_available_items(self, db:AsyncSession, restaurant_id:UUID):
        result = await db.execute(select(MenuItem).where(MenuItem.restaurant_id == restaurant_id, MenuItem.is_available.is_(True)))
        return result.scalars().all()

    async def get_by_restaurant(self,db: AsyncSession,restaurant_id: UUID):
        result = await db.execute(select(MenuItem).where(MenuItem.restaurant_id == restaurant_id))
        return result.scalars().all()