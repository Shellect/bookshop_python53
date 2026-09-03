from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_auth_service
from app.models.user import User
from app.schemas.user import UserCreateRequest, UserLoginRequest, UserResponse
from app.services import AuthService
from app.services.exceptions import AuthenticationError, DuplicateUserError


router = APIRouter(prefix="/auth", tags=["Authentication"])


def _attach_new_session(request: Request, session_id: str) -> None:
    request.state.new_session_id = session_id


def _clear_session(request: Request) -> None:
    request.state.clear_session = True


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user_data: UserCreateRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user, session_id = await auth_service.create_user(user_data)
    except DuplicateUserError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, exc.message) from exc
    _attach_new_session(request, session_id)
    return user


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def login(
    request: Request,
    user_data: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user, session_id = await auth_service.authenticate_user(user_data)
    except AuthenticationError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc
    _attach_new_session(request, session_id)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    await auth_service.logout(request.cookies.get("session_id"))
    _clear_session(request)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    request: Request,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    await auth_service.logout_all(current_user)
    _clear_session(request)
