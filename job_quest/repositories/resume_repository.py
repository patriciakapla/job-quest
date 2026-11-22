from uuid import UUID

from sqlalchemy import desc, select
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

    async def get_user_resumes(self, user_id: UUID) -> list[Resume]:
        query = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(desc(Resume.uploaded_at))
        )
        result = await self.session.scalars(query)

        resume_list = list(result.all())

        return resume_list

    def add(self, resume: Resume):
        self.session.add(resume)

    async def delete(self, resume: Resume) -> None:
        await self.session.delete(resume)
