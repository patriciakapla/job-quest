from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: str
    birth_date: date | None
    created_at: datetime
    updated_at: datetime
