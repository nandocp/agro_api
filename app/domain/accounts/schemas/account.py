from pydantic import BaseModel, field_validator

from app.domain.accounts.enums import AccountPlan


class AccountCreate(BaseModel):
    name: str
    document: str
    plan: AccountPlan

    @field_validator('document')
    @classmethod
    def normalize_document(cls, v: str) -> str:
        return ''.join(filter(str.isdigit, v))
