from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_auth_service
from app.models.user import User
from app.schemas.user import UserCreateRequest, UserLoginRequest, UserResponse
from app.services import AuthService
from app.services.exceptions import AuthenticationError, DuplicateUserError, AlreadyAuthenticatedError


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user_data: UserCreateRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    if getattr(request.state, "is_authenticated", None):
        raise AlreadyAuthenticatedError()
    try:
        current_session_id = getattr(request.state, "session_id")
        user, session_id = await auth_service.create_user(user_data, current_session_id)
    except DuplicateUserError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, exc.message) from exc
    request.state.new_session_id = session_id
    return user


@router.post("/login", response_model=UserResponse)
async def login(
    request: Request,
    user_data: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    if getattr(request.state, "is_authenticated", None):
        raise AlreadyAuthenticatedError()
    try:
        current_session_id = getattr(request.state, "session_id")
        user, session_id = await auth_service.authenticate_user(user_data, current_session_id)
    except AuthenticationError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc
    request.state.new_session_id = session_id
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    if not getattr(request.state, "is_authenticated", None):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is not authenticated")
    await auth_service.logout(getattr(request.state, "session_id"))
    request.state.clear_session = True


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    request: Request,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    if not getattr(request.state, "is_authenticated", None):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is not authenticated")
    await auth_service.logout_all(current_user)
    request.state.clear_session = True
