from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Boolean, Text, Numeric
from datetime import datetime
from decimal import Decimal


class MenuItem(Base):
    __tablename__ = "menu_items"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    name:Mapped[str]=mapped_column(String(100), nullable=False)
    description:Mapped[str|None]=mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255),nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean,default=True,index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean,default=False)
    is_vegetarian: Mapped[bool] = mapped_column(Boolean,default=False)
    preparation_time: Mapped[int] = mapped_column(Integer,default=20)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
