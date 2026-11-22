from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.exceptions import InvalidSalaryRangeError
from job_quest.models.application import Application
from job_quest.schemas.application_schemas import ApplicationCreate
from job_quest.services.application_service import ApplicationService
from tests.factories.application_factory import ApplicationFactory


@pytest.mark.asyncio
async def test_create_application_db(session: AsyncSession, resume, user):
    application = ApplicationFactory(resume_id=resume.id, user_id=user.id)
    session.add(application)
    await session.commit()

    expected_application = {
        'id': application.id,
        'title': application.title,
        'user_id': user.id,
        'company': application.company,
        'location': application.location,
        'description': application.description,
        'notes': application.notes,
        'technologies': application.technologies,
        'resume_id': resume.id,
        'currency_code': application.currency_code,
        'offered_salary_min': application.offered_salary_min,
        'offered_salary_max': application.offered_salary_max,
        'expected_salary_min': application.expected_salary_min,
        'expected_salary_max': application.expected_salary_max,
        'job_posting_url': application.job_posting_url,
        'source_platform': application.source_platform,
        'applied_at': application.applied_at,
        'created_at': application.created_at,
        'updated_at': application.updated_at,
        'status': application.status,
    }

    session.expunge_all()

    application = await session.scalar(
        select(Application).where(Application.id == expected_application['id'])
    )

    assert application is not None
    assert asdict(application) == expected_application


@pytest.mark.asyncio
async def test_application_service_create(session: AsyncSession, user, resume):
    application = ApplicationFactory(resume_id=resume.id, user_id=user.id)

    data = ApplicationCreate(
        title=application.title,
        offered_salary_min=application.offered_salary_min,
        offered_salary_max=application.offered_salary_max,
    )

    service = ApplicationService(session)
    application = await service.create(data, user.id)

    assert application.id is not None
    assert application.user_id == user.id
    assert application.title == data.title
    assert application.offered_salary_min == data.offered_salary_min
    assert application.offered_salary_max == data.offered_salary_max


@pytest.mark.asyncio
async def test_application_create_rejects_invalid_salary_range(user, resume):
    application = ApplicationFactory(resume_id=resume.id, user_id=user.id)
    with pytest.raises(InvalidSalaryRangeError):
        ApplicationCreate(
            title=application.title,
            offered_salary_min=application.offered_salary_max,
            offered_salary_max=application.offered_salary_min,
        )
