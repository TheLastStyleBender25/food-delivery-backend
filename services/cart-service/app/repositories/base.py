from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Generic, TypeVar

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def create(self,db:AsyncSession, obj:ModelType):
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj


    async def get_by_id(self, db:AsyncSession, obj_id):
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalars().one_or_none()


    async def get_all(self, db:AsyncSession):
        result = await db.execute(select(self.model))
        return result.scalars().all()


    async def delete(self, db:AsyncSession, obj:ModelType):
        await db.delete(obj)
        await db.flush()

