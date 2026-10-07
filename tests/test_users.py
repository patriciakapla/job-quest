from dataclasses import asdict
from datetime import date, timedelta

import pytest
from fastapi import status
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
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'google_id': new_user.google_id,
            'birth_date': new_user.birth_date,
            'created_at': time,
            'updated_at': time,
        }

        session.expunge_all()

        user = await session.scalar(
            select(User).where(User.id == expected['id'])
        )

    assert user is not None
    assert asdict(user) == expected


@pytest.mark.asyncio
async def test_update_user(authenticated_client, session: AsyncSession, user):

    updated_user = UserFactory()

    birth_date_json = updated_user.birth_date.isoformat()

    response = authenticated_client.patch(
        '/users/me',
        json={
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'birth_date': birth_date_json,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['first_name'] == updated_user.first_name
    assert response.json()['last_name'] == updated_user.last_name
    assert response.json()['birth_date'] == birth_date_json

    await session.refresh(user)

    assert user.first_name == updated_user.first_name
    assert user.last_name == updated_user.last_name
    assert user.birth_date == updated_user.birth_date


def test_update_user_unauthenticated(client):

    updated_user = UserFactory()

    birth_date_json = updated_user.birth_date.isoformat()

    response = client.patch(
        '/users/me',
        json={
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'birth_date': birth_date_json,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_with_empty_string_name(authenticated_client):

    updated_user = UserFactory()

    birth_date_json = updated_user.birth_date.isoformat()

    response = authenticated_client.patch(
        '/users/me',
        json={
            'first_name': '',
            'last_name': updated_user.last_name,
            'birth_date': birth_date_json,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_user_with_null_name(authenticated_client):

    updated_user = UserFactory()

    birth_date_json = updated_user.birth_date.isoformat()

    response = authenticated_client.patch(
        '/users/me',
        json={
            'first_name': None,
            'last_name': updated_user.last_name,
            'birth_date': birth_date_json,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()['detail'][0]['loc'][1] == 'first_name'
    assert (
        response.json()['detail'][0]['msg']
        == 'Value error, Name cannot be null.'
    )


def test_update_user_with_null_last_name(authenticated_client):

    updated_user = UserFactory()

    birth_date_json = updated_user.birth_date.isoformat()

    response = authenticated_client.patch(
        '/users/me',
        json={
            'first_name': updated_user.first_name,
            'last_name': None,
            'birth_date': birth_date_json,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()['detail'][0]['loc'][1] == 'last_name'
    assert (
        response.json()['detail'][0]['msg']
        == 'Value error, Name cannot be null.'
    )


def test_update_user_with_future_birth_date(authenticated_client):

    updated_user = UserFactory()

    future_birth_date = (date.today() + timedelta(days=1)).isoformat()
    response = authenticated_client.patch(
        '/users/me',
        json={
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'birth_date': future_birth_date,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()['detail'][0]['loc'][1] == 'birth_date'
    assert (
        response.json()['detail'][0]['msg']
        == 'Value error, Birth date cannot be in the future.'
    )


@pytest.mark.asyncio
async def test_delete_user(authenticated_client, session: AsyncSession, user):
    response = authenticated_client.delete('/users/me')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    stored_user = await session.scalar(select(User).where(User.id == user.id))

    assert stored_user is None


def test_delete_user_unauthenticated(client):
    response = client.delete('/users/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
