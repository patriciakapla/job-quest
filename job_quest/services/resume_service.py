from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

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
    ):

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
