from pydantic import BaseModel, ConfigDict, EmailStr


class AuthLogin(BaseModel):
    username: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)
