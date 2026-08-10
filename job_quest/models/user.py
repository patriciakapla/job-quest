from datetime import date, datetime
from uuid import UUID

from sqlalchemy import DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from job_quest.models.base import table_registry


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text('gen_random_uuid()')
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(nullable=False, repr=False)
    birth_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        # NOTE: make the update on db side? (server_onupdate=FetchedValue()
        # and create function on migrations (op.execute(CREATE SQL FUNCTION)))
    )
    # TODO: RELATIONSHIP job_applications: Mapped[list[Application]]
    # TODO: RELATIONSHIP resumes: Mapped[list[Resume]]
