from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    model_config = ConfigDict(rom_attrbutes=True)


class UserPostPayloadSchema(UserBase):
    password: str


class UserPostResponseSchema(UserBase):
    id: UUID4
    created_at: datetime
