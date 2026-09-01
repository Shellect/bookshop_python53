from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from typing import AsyncGenerator

from app.core.config import settings

if settings.testing:
    engine = create_engine( str(settings.database_url))
    SessionLocal = sessionmaker(engine)
else:
    engine = create_async_engine( str(settings.database_url) )
    SessionLocal = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
