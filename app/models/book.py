import uuid
from decimal import Decimal
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Numeric, DateTime, func, CheckConstraint, schema
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import List

from app.core.database import Base

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (CheckConstraint("price >= 0"),{"schema": "catalog"} )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    poster: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    fans: Mapped[List["User"]] = relationship(
        secondary="favorites",
        back_populates="favorites",
        lazy="selectin"
    )