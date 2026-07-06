from app.db.base import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Float, DateTime, Enum, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.restaurant_status import RestaurantStatus
from datetime import time

class Restaurant(Base):
    __tablename__ = "restaurants"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    name:Mapped[String] = mapped_column(String, nullable=False)
    description:Mapped[String] = mapped_column(String, nullable=False)
    phone:Mapped[String] = mapped_column(String, nullable=False)
    address:Mapped[String] = mapped_column(String, nullable=False)
    city:Mapped[String] = mapped_column(String, nullable=False)
    state:Mapped[String] = mapped_column(String, nullable=False)
    status:Mapped[RestaurantStatus] = mapped_column(Enum(RestaurantStatus), nullable=False, default=RestaurantStatus.OPEN)
    latitude: Mapped[float] = mapped_column(Float,nullable=False)
    longitude: Mapped[float] = mapped_column(Float,nullable=False)
    delivery_radius_km: Mapped[float] = mapped_column(Float,nullable=False,default=5.0)
    minimum_order_amount:Mapped[float] = mapped_column(Float,nullable=False, default=0)
    average_preparation_time_minutes:Mapped[int] = mapped_column(Integer,nullable=False, default=20)
    opens_at:Mapped[time] = mapped_column(Time,nullable=False)
    closes_at:Mapped[time] = mapped_column(Time,nullable=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
