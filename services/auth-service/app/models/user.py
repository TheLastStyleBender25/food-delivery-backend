import uuid
from sqlalchemy import String, DateTime, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.enums import UserRole
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[String] = mapped_column(String(255), nullable=False)
    email:Mapped[String] = mapped_column(String(255), unique=True, index=True)
    password_hash:Mapped[String] = mapped_column(String(255))
    role:Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_verified:Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())