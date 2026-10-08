from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.application import Application


class ApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self, user_id: UUID, application_id: UUID
    ) -> Application | None:
        query = (
            select(Application)
            .where(Application.id == application_id)
            .where(Application.user_id == user_id)
        )
        application = await self.session.scalar(query)

        return application

    async def get_user_applications(self, user_id: UUID) -> list[Application]:

        query = (
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(desc(Application.created_at))
        )

        result = await self.session.scalars(query)

        application_list = list(result.all())

        return application_list

    def add(self, application: Application) -> None:
        self.session.add(application)

    async def delete(self, application: Application) -> None:
        await self.session.delete(application)
