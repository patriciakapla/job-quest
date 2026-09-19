from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from authlib.integrations.base_client import OAuthError
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.oauth import oauth
from job_quest.models.user import User
from tests.factories.user_factory import UserFactory


def test_login_with_google_redirects_to_google(client, monkeypatch):
    authorize_redirect = AsyncMock(
        return_value=RedirectResponse(
            url='https://accounts.google.com/',
            status_code=HTTPStatus.FOUND,
        )
    )

    monkeypatch.setattr(
        oauth.google,
        'authorize_redirect',
        authorize_redirect,
    )

    response = client.get('/auth/google', follow_redirects=False)

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['location'] == 'https://accounts.google.com/'

    authorize_redirect.assert_awaited_once()
    await_call = authorize_redirect.await_args
    assert await_call is not None

    _, callback_url = await_call.args

    assert str(callback_url) == 'http://testserver/auth/google/callback'


@pytest.mark.asyncio
async def test_google_callback_creates_user(
    client, session: AsyncSession, monkeypatch
):
    profile = UserFactory.build()

    authorize_access_token = AsyncMock(
        return_value={
            'userinfo': {
                'sub': profile.google_id,
                'email': profile.email,
                'email_verified': True,
                'given_name': profile.first_name,
                'family_name': profile.last_name,
            }
        }
    )

    monkeypatch.setattr(
        oauth.google, 'authorize_access_token', authorize_access_token
    )

    response = client.get('/auth/google/callback', follow_redirects=False)

    assert response.status_code == HTTPStatus.SEE_OTHER
    assert response.headers['location'] == '/'
    assert client.cookies.get('session') is not None
    authorize_access_token.assert_awaited_once()

    session.expunge_all()

    stored_user = await session.scalar(
        select(User).where(User.google_id == profile.google_id)
    )

    assert stored_user is not None
    assert stored_user.email == profile.email
    assert stored_user.first_name == profile.first_name
    assert stored_user.last_name == profile.last_name
    assert stored_user.birth_date is None


def test_google_callback_handles_oauth_error(client, monkeypatch):
    authorize_access_token = AsyncMock(
        side_effect=OAuthError(error='access_denied')
    )

    monkeypatch.setattr(
        oauth.google,
        'authorize_access_token',
        authorize_access_token,
    )

    response = client.get('/auth/google/callback')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Google authentication failed.'}
    authorize_access_token.assert_awaited_once()


def test_google_callback_rejects_missing_userinfo(client, monkeypatch):
    authorize_access_token = AsyncMock(return_value={})

    monkeypatch.setattr(
        oauth.google,
        'authorize_access_token',
        authorize_access_token,
    )

    response = client.get('/auth/google/callback')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Google account information is missing.'
    }
    assert client.cookies.get('session') is None
    authorize_access_token.assert_awaited_once()


def test_google_callback_rejects_unverified_email(client, monkeypatch):
    profile = UserFactory.build()

    authorize_access_token = AsyncMock(
        return_value={
            'userinfo': {
                'sub': profile.google_id,
                'email': profile.email,
                'email_verified': False,
                'given_name': profile.first_name,
                'family_name': profile.last_name,
            }
        }
    )

    monkeypatch.setattr(
        oauth.google,
        'authorize_access_token',
        authorize_access_token,
    )

    response = client.get('/auth/google/callback')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Google did not provide a complete verified profile.'
    }
    assert client.cookies.get('session') is None
    authorize_access_token.assert_awaited_once()
