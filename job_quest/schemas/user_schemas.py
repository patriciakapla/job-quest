from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: str
    birth_date: date | None
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    birth_date: date | None = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def names_cannot_be_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError('Name cannot be null.')

        return value

    @field_validator('birth_date')
    @classmethod
    def birth_dates_cant_be_future(cls, value: date | None) -> date | None:

        if value is not None and value > date.today():
            raise ValueError('Birth date cannot be in the future.')

        return value
