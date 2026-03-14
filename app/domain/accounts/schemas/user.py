from pydantic import BaseModel, EmailStr

from app.shared.schemas import BaseSchema


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseSchema):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None
