from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResumePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    size_bytes: int
    uploaded_at: datetime


class ResumeCreate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=150)


class ResumeUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=150)

    @field_validator('name')
    @classmethod
    def name_cant_be_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Resume name can't be null")
        return value
