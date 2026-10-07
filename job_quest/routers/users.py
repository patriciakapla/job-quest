from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.database import get_session
from job_quest.core.security import get_current_user
from job_quest.models.user import User
from job_quest.schemas.user import UserPublic, UserUpdate
from job_quest.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])
DB_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.patch('/me', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user(
    data: UserUpdate, session: DB_Session, current_user: CurrentUser
):
    service = UserService(session)

    return await service.update(current_user, data)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Request, session: DB_Session, current_user: CurrentUser
):
    service = UserService(session)

    await service.delete(current_user)

    request.session.clear()
