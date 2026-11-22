from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.core.database import get_session
from job_quest.core.security import get_current_user
from job_quest.models.user import User
from job_quest.schemas.resume_schemas import ResumeCreate, ResumePublic
from job_quest.services.resume_service import ResumeService

router = APIRouter(prefix='/resumes', tags=['resumes'])
current_user = Annotated[User, Depends(get_current_user)]
DB_Session = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    '/', response_model=ResumePublic, status_code=status.HTTP_201_CREATED
)
async def create_resume(
    session: DB_Session, current_user: current_user, data: ResumeCreate
):

    # TODO: IMPLEMENT FILE UPLOAD TO STORAGE
    random_object_key = str(uuid4())
    size_bytes = 200
    service = ResumeService(session)

    return await service.create(
        data, current_user.id, random_object_key, size_bytes
    )
