import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Numeric, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.base import Base
from sqlalchemy.sql import func
from app.models.order_status import OrderStatus
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    customer_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    restaurant_id:Mapped[UUID]=mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    total_amount:Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    status:Mapped[OrderStatus]=mapped_column(Enum(OrderStatus), default=OrderStatus.PLACED, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items:Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


