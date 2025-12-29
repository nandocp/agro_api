from pydantic import UUID4, BaseModel, EmailStr, datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserPostPayloadSchema(BaseModel):
    password: str


class UserGetResponseSchema(UserBase):
    id: UUID4
    created_at: datetime
