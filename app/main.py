from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_session_service
from app.middleware.session_middleware import SessionMiddleware
from app.models.book import Book
from app.models.user import User
from app.routers import auth
from app.schemas.book import BookResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, session_service=get_session_service)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books", response_model=List[BookResponse])
async def get_books(page: int = 0, db: AsyncSession = Depends(get_db)):
    books_list = await db.scalars(
        select(Book)
        .offset(page * 10)
        .limit(10)
        .order_by(Book.created_at.desc())
    )
    return books_list.all()

