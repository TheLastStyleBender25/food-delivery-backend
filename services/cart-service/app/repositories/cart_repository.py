from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from sqlalchemy import select
from uuid import UUID
from app.models.cart_item import CartItem


class CartRepository(BaseRepository[CartItem]):

    def __init__(self):
        super().__init__(CartItem)


    async def get_customer_cart(self, db:AsyncSession, customer_id:UUID):
        result = await db.execute(select(self.model).where(self.model.customer_id == customer_id))
        return result.scalars().all()

    async def get_cart_item(self, db:AsyncSession, customer_id:UUID, menu_item_id:UUID):
        result = await db.execute(select(self.model).where(self.model.customer_id == customer_id, self.model.menu_item_id == menu_item_id))
        return result.scalars().one_or_none()

    async def clear_cart(self, db:AsyncSession, customer_id:UUID):
        result = await db.execute(select(self.model).where(self.model.customer_id == customer_id))
        items = result.scalars().all()
        for item in items:
            await db.delete(item)

        await db.flush()
