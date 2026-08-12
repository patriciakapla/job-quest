from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.user import User
from tests.factories.user_factory import UserFactory


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = UserFactory()
        session.add(new_user)
        await session.commit()

        expected = {
            'id': new_user.id,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'password_hash': new_user.password_hash,
            'birth_date': new_user.birth_date,
            'created_at': time,
            'updated_at': time,
        }

        session.expunge_all()

        user = await session.scalar(
            select(User).where(User.username == expected['username'])
        )

    assert user is not None
    assert asdict(user) == expected
