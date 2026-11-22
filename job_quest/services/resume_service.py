from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.exceptions import ResumeNotFoundError
from job_quest.models.resume import Resume
from job_quest.repositories.resume_repository import ResumeRepository
from job_quest.schemas.resume_schemas import ResumeCreate


class ResumeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.resume = ResumeRepository(session)

    async def create(
        self,
        data: ResumeCreate,
        user_id: UUID,
        object_key: str,
        size_bytes: int,
    ) -> Resume:

        resume_data = data.model_dump(exclude_unset=True)

        resume = Resume(
            **resume_data,
            user_id=user_id,
            object_key=object_key,
            size_bytes=size_bytes,
        )

        self.resume.add(resume)
        await self.session.commit()
        await self.session.refresh(resume)
        return resume

    async def get_by_id(self, user_id: UUID, resume_id: UUID) -> Resume:

        resume = await self.resume.get_by_id(user_id, resume_id)

        if resume is None:
            raise ResumeNotFoundError()

        return resume

    async def get_resume_list(self, user_id: UUID) -> list[Resume]:

        resume_list = await self.resume.get_user_resumes(user_id)

        return resume_list

    async def delete_resume(self, user_id: UUID, resume_id: UUID) -> None:
        resume = await self.resume.get_by_id(user_id, resume_id)

        if resume is None:
            raise ResumeNotFoundError()

        await self.resume.delete(resume)
        await self.session.commit()
