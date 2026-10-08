from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from job_quest.models.status import Status


class ApplicationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    resume_id: UUID | None
    company: str | None
    location: str | None
    description: str | None
    notes: str | None
    technologies: str | None
    currency_code: str | None
    offered_salary_min: Decimal | None
    offered_salary_max: Decimal | None
    expected_salary_min: Decimal | None
    expected_salary_max: Decimal | None
    job_posting_url: str | None
    source_platform: str | None
    applied_at: date | None
    created_at: datetime
    updated_at: datetime
    status: Status


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=150)
    resume_id: UUID | None = None
    company: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=100)
    description: str | None = None
    notes: str | None = None
    technologies: str | None = Field(default=None, max_length=300)
    currency_code: str | None = Field(default=None, min_length=3, max_length=3)
    offered_salary_min: Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2, ge=0
    )
    offered_salary_max: Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2, ge=0
    )
    expected_salary_min: Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2, ge=0
    )
    expected_salary_max: Decimal | None = Field(
        default=None, max_digits=12, decimal_places=2, ge=0
    )
    job_posting_url: str | None = None
    source_platform: str | None = Field(default=None, max_length=100)
    applied_at: date | None = None
    status: Status = Status.SAVED

    @model_validator(mode='after')
    def validate_salary_range(self):
        ranges = {
            'expected': (self.expected_salary_min, self.expected_salary_max),
            'offered': (self.offered_salary_min, self.offered_salary_max),
        }

        for name, (minimum, maximum) in ranges.items():
            if (
                minimum is not None
                and maximum is not None
                and maximum < minimum
            ):
                raise ValueError(
                    f"{name.capitalize()} minimum salary can't be greater than"
                    f' {name} maximum salary'
                )
        return self

    @field_validator('applied_at')
    @classmethod
    def applied_at_cant_be_in_future(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("Application date can't be a future date")
        return value
