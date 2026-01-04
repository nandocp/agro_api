from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from agro_api.schemas.common import BaseSchema


class UserBase(BaseModel):
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attrbutes=True)


class UserCreate(UserBase):
    password: str


class UserItem(UserBase, BaseSchema):
    last_sign_in_at: datetime
    current_sign_in_at: datetime
    is_active: bool


class UserUpdate(BaseModel):
    name: str
