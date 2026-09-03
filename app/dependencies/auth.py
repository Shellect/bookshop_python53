from fastapi import Depends, HTTPException, Request, status

from app.dependencies.services import get_user_service
from app.models.user import User, UserRole
from app.services.user_service import UserService


async def get_current_user(request: Request, user_service: UserService = Depends(get_user_service)) -> User:
    # Проверяем есть ли user_id в request.state
    # это устанавливается в SessionMiddleware
    if getattr(request.state, "is_authenticated", False):
        user = await user_service.get_by_id(request.state.user_id)
        if user :
            return user
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")


async def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.is_active:
        return current_user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "User account is disabled")


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role == UserRole.ADMIN:
        return current_user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")
