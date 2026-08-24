import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Mapped, mapped_column
from sqlalchemy.dialects.postgres import UUID as PG_UUID
from app.core.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

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
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True),
        server_default=func.now(),
        nullable=False
    )