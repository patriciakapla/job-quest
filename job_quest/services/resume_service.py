from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.exceptions import ResumeNotFoundError, UserLimitExceeded
from job_quest.models.resume import Resume
from job_quest.repositories.resume_repository import ResumeRepository
from job_quest.schemas.resume_schemas import ResumeCreate

USER_STORAGE_LIMIT_BYTES = 10 * 1024 * 1024


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

        storage_usage = await self.check_storage_usage(user_id)
        updated_usage = storage_usage + resume.size_bytes
        if updated_usage > USER_STORAGE_LIMIT_BYTES:
            raise UserLimitExceeded()

        """
        TODO:

        adicionar contador storage_used_bytes no usuário
        antes do upload fazer reserva atômica
        ao apagar resume subtrair tamanho do contador.
        se upload falhar, desfazer reserva

        adicionar tabela de storage total
        se upload chegar no limite, impedir upload
        """

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

    async def delete_resume(
        self, user_id: UUID, resume_id: UUID
    ) -> int | None:
        resume = await self.resume.get_by_id(user_id, resume_id)

        if resume is None:
            raise ResumeNotFoundError()

        await self.resume.delete(resume)
        await self.session.commit()

    async def check_storage_usage(self, user_id: UUID):
        resume_list = await self.get_resume_list(user_id)
        return sum(resume.size_bytes for resume in resume_list)
