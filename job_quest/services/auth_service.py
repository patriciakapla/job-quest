from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.user import User
from job_quest.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def get_or_create_google_user(
        self, google_id: str, email: str, first_name: str, last_name: str
    ) -> User:
        user = await self.users.get_by_google_id(google_id)

        if user is not None:
            return user

        user = User(
            google_id=google_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        self.users.add(user)

        await self.session.commit()

        await self.session.refresh(user)

        return user
