from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.resume import Resume
from tests.factories.resume_factory import ResumeFactory


@pytest.mark.asyncio
async def test_create_resume(session: AsyncSession, user):
    resume = ResumeFactory(user_id=user.id)
    session.add(resume)
    await session.commit()
    expected_resume = {
        'id': resume.id,
        'user_id': user.id,
        'name': resume.name,
        'object_key': resume.object_key,
        'size_bytes': resume.size_bytes,
        'uploaded_at': resume.uploaded_at,
    }

    session.expunge_all()

    resume = await session.scalar(
        select(Resume).where(Resume.id == expected_resume['id'])
    )

    assert resume is not None
    assert asdict(resume) == expected_resume
