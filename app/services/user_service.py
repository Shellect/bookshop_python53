from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreateRequest
from app.services.exceptions import DuplicateUserError


class UserService:
    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, user_data: UserCreateRequest, hashed_password: str) -> User:
        if await self.get_by_email(user_data.email):
            raise DuplicateUserError("email", "Email is already registered")

        if await self.get_by_name(user_data.login):
            raise DuplicateUserError("login", "Username is already taken")

        user = User(
            email=user_data.email,
            username=user_data.login,
            hashed_password=hashed_password,
        )

        self.database.add(user)
        await self.database.commit()
        await self.database.refresh(user)

        return user

    async def get_all(self) -> List[User]:
        query = select(User).where(User.is_active).limit(10)
        result = await self.database.scalars(query)
        return result.all()

    async def get_by_id(self, id) -> Optional[User]:
        return await self.database.get(User, id)

    async def get_by_name(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.database.scalars(query)
        return result.first()

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.database.scalars(query)
        return result.first()

    async def update_last_login(self, user: User):
        user.last_login = datetime.now(timezone.utc)
        await self.database.commit()
        await self.database.refresh(user)
