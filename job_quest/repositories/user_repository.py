from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.user import User
from job_quest.schemas.user import UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        return await self.session.scalar(query)

    async def get_by_google_id(self, google_id: str) -> User | None:
        query = select(User).where(User.google_id == google_id)
        return await self.session.scalar(query)

    def add(self, user: User) -> None:
        self.session.add(user)

    async def delete(self, user: User) -> None:
        await self.session.delete(user)

    @staticmethod
    def update(user: User, data: UserUpdate) -> User:
        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(user, field, value)

        return user
