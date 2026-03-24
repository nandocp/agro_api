from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.shared.schemas import BaseSchema, Pagination


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None


class UserFilters(Pagination):
    name: str | None = Field(None)
    email: str | None = Field(None)
    deactivated_at: datetime | None = Field(None)
    is_active: bool | None = Field(None)
    account_id: UUID | None = Field(None)
