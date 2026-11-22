from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.exceptions import (
    ApplicationNotFoundError,
    InvalidSalaryRangeError,
    ResumeNotFoundError,
)
from job_quest.models.application import Application
from job_quest.repositories.application_repository import ApplicationRepository
from job_quest.repositories.resume_repository import ResumeRepository
from job_quest.schemas.application_schemas import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.applications = ApplicationRepository(session)
        self.resumes = ResumeRepository(session)

    async def create(self, data: ApplicationCreate, user_id: UUID):
        application_data = data.model_dump(exclude_unset=True)

        resume_id = application_data.get('resume_id')

        await self._validate_resume(user_id, resume_id)

        offered_min = application_data.get('offered_salary_min')
        offered_max = application_data.get('offered_salary_max')

        expected_min = application_data.get('expected_salary_min')

        expected_max = application_data.get('expected_salary_max')

        self._validate_salary_range('expected', expected_min, expected_max)
        self._validate_salary_range('offered', offered_min, offered_max)

        application = Application(**application_data, user_id=user_id)
        self.applications.add(application)

        await self.session.commit()
        await self.session.refresh(application)

        return application

    async def update(
        self,
        data: ApplicationUpdate,
        user_id: UUID,
        application_id: UUID,
    ) -> Application:

        application = await self.applications.get_by_id(
            user_id=user_id,
            application_id=application_id,
        )

        if application is None:
            raise ApplicationNotFoundError()

        update = data.model_dump(exclude_unset=True)

        resume_id = update.get('resume_id', application.resume_id)

        await self._validate_resume(user_id, resume_id)

        offered_min = update.get(
            'offered_salary_min', application.offered_salary_min
        )
        offered_max = update.get(
            'offered_salary_max', application.offered_salary_max
        )

        expected_min = update.get(
            'expected_salary_min', application.expected_salary_min
        )

        expected_max = update.get(
            'expected_salary_max', application.expected_salary_max
        )

        self._validate_salary_range('expected', expected_min, expected_max)
        self._validate_salary_range('offered', offered_min, offered_max)

        for field, value in update.items():
            setattr(application, field, value)

        await self.session.commit()
        await self.session.refresh(application)

        return application

    async def get_application_by_id(self, user_id: UUID, application_id: UUID):
        application = await self.applications.get_by_id(
            user_id, application_id
        )

        if application is None:
            raise ApplicationNotFoundError()

        return application

    async def get_application_list(self, user_id: UUID):

        application_list = await self.applications.get_user_applications(
            user_id
        )
        return application_list

    @staticmethod
    def _validate_salary_range(
        salary_type: str, minimum: Decimal | None, maximum: Decimal | None
    ) -> None:
        if minimum is not None and maximum is not None and maximum < minimum:
            raise InvalidSalaryRangeError(salary_type)

    async def _validate_resume(
        self, user_id: UUID, resume_id: UUID | None
    ) -> None:

        if resume_id is None:
            return

        resume = await self.resumes.get_by_id(
            user_id=user_id,
            resume_id=resume_id,
        )

        if resume is None:
            raise ResumeNotFoundError()
