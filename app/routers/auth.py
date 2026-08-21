from fastapi import APIRouter, Depends, Request, status

from app.dependencies.services import get_auth_service
from app.services import AuthService
from app.schemas.user import UserCreateRequest, UserLoginRequest, UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user_data: UserCreateRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.create_user(user_data, request)
    return user

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def login(
    user_data: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(user_data, request)
    return user

