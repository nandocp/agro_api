from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.domain.accounts.enums import UserRole
from app.shared.schemas import BaseSchema, Pagination


class UserCreateForm(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = Field(default=UserRole.WORKER)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    account_id: UUID
    password: str


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
