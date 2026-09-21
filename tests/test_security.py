from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.security import get_current_user
from job_quest.models.user import User


@pytest.mark.asyncio
async def test_get_current_user_returns_authenticated_user(
    session: AsyncSession, user: User
):
    request = Request({'type': 'http', 'session': {'user_id': str(user.id)}})

    current_user = await get_current_user(request, session)

    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_current_user_rejects_non_uuid_user_id(
    session: AsyncSession,
):
    request = Request({'type': 'http', 'session': {'user_id': 'invalid uuid'}})

    with pytest.raises(HTTPException) as error:
        await get_current_user(request, session)

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == 'Authentication required.'
    assert request.session == {}


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_user_id(
    session: AsyncSession,
):
    request = Request({'type': 'http', 'session': {}})

    with pytest.raises(HTTPException) as error:
        await get_current_user(request, session)

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == 'Authentication required.'
    assert request.session == {}


@pytest.mark.asyncio
async def test_get_current_user_rejects_non_existent_user_id(
    session: AsyncSession,
):
    request = Request({
        'type': 'http',
        'session': {'user_id': str(uuid4())},
    })

    with pytest.raises(HTTPException) as error:
        await get_current_user(request, session)

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == 'Authentication required.'
    assert request.session == {}
