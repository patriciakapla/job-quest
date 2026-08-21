from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.application import Application
from tests.factories.application_factory import ApplicationFactory


@pytest.mark.asyncio
async def test_create_application(session: AsyncSession, resume):
    application = ApplicationFactory(resume_id=resume.id)
    session.add(application)
    await session.commit()

    expected_application = {
        'id': application.id,
        'title': application.title,
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
