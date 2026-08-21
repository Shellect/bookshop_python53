from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User, UserRole

async def get_current_user(request: Request, database: AsyncSession = Depends(get_db)) -> User:
    # Проверяем есть ли user_id в request.state
    # это устанавливается в SessionMiddleware
    if request.state.is_authenticated:
        user_id = request.state.user_id
        return await database.get(User, user_id)
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")


async def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.is_active:
        return current_user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "User account is disabled")

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        return current_user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")