from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from job_quest.models.base import table_registry
from job_quest.models.status import Status


@mapped_as_dataclass(table_registry)
class Application:
    __tablename__ = 'applications'
    __table_args__ = (
        CheckConstraint(
            '(expected_salary_min IS NULL OR expected_salary_min >= 0) AND '
            '(expected_salary_max IS NULL OR expected_salary_max >= 0) AND '
            '(expected_salary_min IS NULL OR expected_salary_max IS NULL OR '
            'expected_salary_min <= expected_salary_max)',
            name='check_expected_salary',
        ),
        CheckConstraint(
            '(offered_salary_min IS NULL OR offered_salary_min >= 0) AND '
            '(offered_salary_max IS NULL OR offered_salary_max >= 0) AND '
            '(offered_salary_min IS NULL OR offered_salary_max IS NULL OR '
            'offered_salary_min <= offered_salary_max)',
            name='check_offered_salary',
        ),
    )

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text('gen_random_uuid()')
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    resume_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('resumes.id'), default=None
    )
    company: Mapped[str | None] = mapped_column(String(100), default=None)
    location: Mapped[str | None] = mapped_column(String(100), default=None)
    description: Mapped[str | None] = mapped_column(default=None)
    notes: Mapped[str | None] = mapped_column(default=None)
    technologies: Mapped[str | None] = mapped_column(String(300), default=None)
    currency_code: Mapped[str | None] = mapped_column(CHAR(3), default=None)
    offered_salary_min: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), default=None
    )
    offered_salary_max: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), default=None
    )
    expected_salary_min: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), default=None
    )
    expected_salary_max: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), default=None
    )
    job_posting_url: Mapped[str | None] = mapped_column(default=None)
    source_platform: Mapped[str | None] = mapped_column(
        String(100), default=None
    )
    applied_at: Mapped[date | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name='status_enum',
            native_enum=True,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        default=Status.SAVED,
    )
