from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Numeric
from decimal import Decimal


class CartItem(Base):
    __tablename__ = "cart_items"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    restaurant_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    menu_item_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    quantity:Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price_at_addition:Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())