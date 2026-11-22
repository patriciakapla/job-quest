from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.database import get_session
from job_quest.core.security import get_current_user
from job_quest.models.user import User
from job_quest.schemas.application_schemas import (
    ApplicationCreate,
    ApplicationPublic,
    ApplicationUpdate,
)
from job_quest.services.application_service import ApplicationService

router = APIRouter(prefix='/applications', tags=['applications'])
DB_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', response_model=ApplicationPublic, status_code=status.HTTP_201_CREATED
)
async def create_job_application(
    session: DB_Session, current_user: CurrentUser, data: ApplicationCreate
):
    service = ApplicationService(session)

    return await service.create(data, current_user.id)


@router.patch(
    '/{application_id}',
    response_model=ApplicationPublic,
    status_code=status.HTTP_200_OK,
)
async def update_job_application(
    session: DB_Session,
    current_user: CurrentUser,
    data: ApplicationUpdate,
    application_id: UUID,
):
    service = ApplicationService(session)

    return await service.update(data, current_user.id, application_id)


@router.get(
    '/{application_id}',
    response_model=ApplicationPublic,
    status_code=status.HTTP_200_OK,
)
async def get_application_by_id(
    session: DB_Session,
    current_user: CurrentUser,
    application_id: UUID,
):
    service = ApplicationService(session)

    return await service.get_application_by_id(current_user.id, application_id)


@router.get(
    '/', response_model=list[ApplicationPublic], status_code=status.HTTP_200_OK
)
async def get_application_list(
    session: DB_Session,
    current_user: CurrentUser,
):
    service = ApplicationService(session)

    return await service.get_application_list(current_user.id)


@router.delete('/{application_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    session: DB_Session, current_user: CurrentUser, application_id: UUID
):
    service = ApplicationService(session)

    await service.delete_application(current_user.id, application_id)
