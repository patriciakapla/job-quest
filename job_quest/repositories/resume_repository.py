from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.resume import Resume


class ResumeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID, resume_id: UUID) -> Resume | None:
        query = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .where(Resume.id == resume_id)
        )
        resume = await self.session.scalar(query)

        return resume
