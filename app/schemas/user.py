from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr, model_validator

from app.models.user import UserRole

class UserCreateRequest(BaseModel):
    email: EmailStr
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str

    @model_validator(mode='after')
    def validate_password(self) -> 'CreateUserRequest':
        if self.password != self.confirm.password:
            raise ValueError('Passwords do not match')
        return self


class UserLoginRequest(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes = True,
        extra= "forbid",
        str_strip_whitespace=True
    )

