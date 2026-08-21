from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreateRequest

class UserService:
    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, user_data: UserCreateRequest, hashed_password: str) -> User:
        if await self.get_by_email(user_data.email):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is already registered")

        if await self.get_by_name(user_data.login):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username is already taken")

        user = User(
            email = user_data.email,
            username = user_data.login,
            hash_password = hashed_password,
        )

        self.database.add(user)
        await self.database.commit()
        await self.database.refresh(user)

        return user

    async def get_by_id(self, id) -> User:
        return await self.database.get(User, id)

    async def get_by_name(self, username: str) -> Optional[User]:
        query =  select(User).where(User.username == username)
        return await self.database.execute(query).first()

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        return await self.database.execute(query).first()


