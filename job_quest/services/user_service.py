from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.user import User
from job_quest.repositories.user_repository import UserRepository
from job_quest.schemas.user import UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def update(self, user: User, data: UserUpdate) -> User:
        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        await self.users.delete(user)
        await self.session.commit()
