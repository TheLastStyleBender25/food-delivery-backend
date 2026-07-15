from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):

    def __init__(self):
        super().__init__(OrderItem)

    async def get_order_items(self,db: AsyncSession,order_id: UUID):
        result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return result.scalars().all()