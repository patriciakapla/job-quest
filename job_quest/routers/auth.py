from typing import Annotated

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.database import get_session
from job_quest.core.oauth import oauth
from job_quest.core.security import get_current_user
from job_quest.models.user import User
from job_quest.schemas.user import UserPublic
from job_quest.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

DB_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/google')
async def login_with_google(request: Request):
    callback_url = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, callback_url)


@router.get('/google/callback', name='google_callback')
async def google_callback(request: Request, session: DB_Session):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Google authentication failed.',
        ) from error

    userinfo = token.get('userinfo')

    if not isinstance(userinfo, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Google account information is missing.',
        )

    google_id = userinfo.get('sub')
    email = userinfo.get('email')
    email_verified = userinfo.get('email_verified')
    first_name = userinfo.get('given_name')
    last_name = userinfo.get('family_name')

    if (
        not isinstance(google_id, str)
        or not isinstance(email, str)
        or not isinstance(first_name, str)
        or not isinstance(last_name, str)
        or email_verified is not True
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Google did not provide a complete verified profile.',
        )

    auth_service = AuthService(session)

    user = await auth_service.get_or_create_google_user(
        google_id=google_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    request.session.clear()
    request.session['user_id'] = str(user.id)

    return RedirectResponse(
        url='/',
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get('/me', response_model=UserPublic)
async def get_me(current_user: CurrentUser) -> User:
    return current_user


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request) -> None:
    request.session.clear()
