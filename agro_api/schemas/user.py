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


class UserGetResponseSchema(UserPostResponseSchema):
    last_sign_in_at: datetime
    current_sign_in_at: datetime
    is_active: bool


class UserUpdateResponseSchema(UserPostResponseSchema):
    updated_at: datetime


class UserUpdatePayloadSchema(BaseModel):
    name: str
