from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#############Generic Repository Pattern
# TypeVar creates a placeholder type "ModelType"
# It can represent ANY model class (Category, MenuItem, User, etc.)
# Think of it as a variable for types instead of values
ModelType = TypeVar("ModelType")


# Generic[ModelType] means this class is "parameterized" by a type.
# Generic[ModelType] means this class is "parameterized" by a type.
# When you write BaseRepository[Category], ModelType becomes Category everywhere.
# This gives you type safety and IDE autocomplete for whichever model you pass in.
class BaseRepository(Generic[ModelType]):

    def __init__(self, model:type[ModelType]):
        # Stores the actual model CLASS (not an instance) so we can
        # run queries like db.query(self.model) later.
        # e.g. if you do BaseRepository(Category), self.model = Category
        self.model = model

    async def create(self, db: AsyncSession, obj: ModelType):
        # Stage the new object — tells SQLAlchemy to track this object
        # but doesn't hit the DB yet
        db.add(obj)

        # Write to the database and finalize the transaction
        await db.flush()

        # Re-fetch the object from DB into memory so that
        # DB-generated fields (id, created_at, etc.) are populated on the object
        await db.refresh(obj)

        return obj

    async def get_by_id(self, db: AsyncSession, obj_id):
        # db.query(self.model)     → SELECT * FROM <model's table>
        # .filter(...)             → WHERE id = obj_id
        # .first()                 → LIMIT 1, returns the object or None if not found
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession):
        # SELECT * FROM <model's table> with no filters
        # Returns a list of all rows as model objects, empty list if none
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, obj: ModelType):
        # Mark the object for deletion — doesn't hit DB yet
        await db.delete(obj)

        # Commit the transaction — row is now permanently removed from DB
        await db.flush()
        # Note: no refresh needed here since the object no longer exists in DB