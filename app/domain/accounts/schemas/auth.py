from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: EmailStr
    password: str
    account_id: UUID


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
