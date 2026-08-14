from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from job_quest.models.base import table_registry


@mapped_as_dataclass(table_registry)
class Answer:
    __tablename__ = 'answers'

    id: Mapped[UUID] = mapped_column(
        init=False, server_default=text('gen_random_uuid()'), primary_key=True
    )
    description: Mapped[str]
    answer: Mapped[str]
