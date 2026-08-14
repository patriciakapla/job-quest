import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job_quest.models.answer import Answer
from tests.factories.answer_factory import AnswerFactory


@pytest.mark.asyncio
async def test_create_answer(session: AsyncSession):
    answer = AnswerFactory()
    session.add(answer)
    await session.commit()

    expected_answer = {
        'id': answer.id,
        'description': answer.description,
        'answer': answer.answer,
    }

    session.expunge_all()

    answer = await session.scalar(
        select(Answer).where(Answer.id == expected_answer['id'])
    )
