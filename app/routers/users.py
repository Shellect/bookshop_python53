from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_user_service
from app.schemas.user import UserResponse
from app.services.user_service import UserService


router = APIRouter(prefix="/user", tags=["User"])

@router.get("", response_model=List[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()