import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Numeric, Enum, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.base import Base
from sqlalchemy.sql import func
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.order import Order


class OrderItem(Base):
    __tablename__ = "order_items"

    id:Mapped[UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("orders.id"),nullable=False)
    menu_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),nullable=False)
    name: Mapped[str] = mapped_column(String,nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_order: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order:Mapped["Order"] = relationship(back_populates="items")