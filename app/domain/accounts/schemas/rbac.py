from uuid import UUID

from pydantic import BaseModel

from app.domain.accounts.enums import UserRole


class UserRoleCreate(BaseModel):
    user_id: UUID
    role: UserRole
