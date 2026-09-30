from datetime import datetime
import uuid

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base

class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = (CheckConstraint("quantity > 0", name="cart_quantity_check"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("catalog.books.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )