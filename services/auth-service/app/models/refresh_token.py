import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token_hash:Mapped[String] = mapped_column(String, nullable=False)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
