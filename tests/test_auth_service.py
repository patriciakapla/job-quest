import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.user import User
from job_quest.services.auth_service import AuthService
from tests.factories.user_factory import UserFactory


@pytest.mark.asyncio
async def test_creates_google_user(session: AsyncSession):
    service = AuthService(session)
    candidate = UserFactory.build()

    user = await service.get_or_create_google_user(
        google_id=candidate.google_id,
        email=candidate.email,
        first_name=candidate.first_name,
        last_name=candidate.last_name,
    )

    assert user.google_id == candidate.google_id
    assert user.email == candidate.email
    assert user.first_name == candidate.first_name
    assert user.last_name == candidate.last_name
    assert user.birth_date is None
    assert user.id is not None

    session.expunge_all()

    stored_user = await session.scalar(
        select(User).where(User.google_id == candidate.google_id)
    )

    assert stored_user is not None
    assert stored_user.id == user.id


@pytest.mark.asyncio
async def test_google_user_already_exists(session: AsyncSession, user: User):
    service = AuthService(session)

    candidate = await service.get_or_create_google_user(
        google_id=user.google_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    assert user.google_id == candidate.google_id
    assert user.email == candidate.email
    assert user.first_name == candidate.first_name
    assert user.last_name == candidate.last_name
    assert user.id == candidate.id
    assert user.birth_date == candidate.birth_date
