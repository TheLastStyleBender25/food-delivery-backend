from celery.bin.result import result
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from sqlalchemy import select
from uuid import UUID
from app.models.order import Order
from sqlalchemy.orm import selectinload


class OrderRepository(BaseRepository[Order]):

    def __init__(self):
        super().__init__(Order)

    async def get_customer_orders(self, db: AsyncSession, customer_id: UUID):
        result = await db.execute(select(Order).where(Order.customer_id == customer_id).order_by(Order.created_at.desc()))
        return result.scalars().all()

    async def get_restaurant_orders(self, db: AsyncSession, restaurant_id: UUID):
        result = await db.execute(select(Order).where(Order.restaurant_id == restaurant_id).order_by(Order.created_at.desc()))
        return result.scalars().all()

    async def get_customer_order(self, db: AsyncSession, order_id: UUID, customer_id: UUID):
        result = await db.execute(select(Order).options(selectinload(Order.items)).where(Order.id == order_id,Order.customer_id == customer_id,))
        return result.scalars().one_or_none()

    async def get_restaurant_order(self,db: AsyncSession,order_id: UUID,restaurant_id: UUID):
        result = await db.execute(select(Order).options(selectinload(Order.items)).where( Order.id == order_id,Order.restaurant_id == restaurant_id))
        return result.scalars().one_or_none()
