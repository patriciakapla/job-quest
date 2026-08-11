from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from job_quest.models.base import table_registry


@mapped_as_dataclass(table_registry)
class Resume:
    __tablename__ = 'resumes'
    __table_args__ = (
        CheckConstraint(
            'size_bytes > 0 AND size_bytes <= (2 * 1024 * 1024)',
            # limit = 2mb
            name='check_size_positive_and_in_limit',
        ),
    )

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text('gen_random_uuid()')
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    object_key: Mapped[str] = mapped_column(nullable=False, unique=True)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
