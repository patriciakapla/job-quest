from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.database import get_session
from job_quest.models.user import User
from job_quest.repositories.user_repository import UserRepository


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User:
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Authentication required.',
    )

    raw_user_id = request.session.get('user_id')

    if not isinstance(raw_user_id, str):
        raise auth_error

    try:
        user_id = UUID(raw_user_id)
    except ValueError:
        request.session.clear()
        raise auth_error

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)

    if user is None:
        request.session.clear()
        raise auth_error

    return user
