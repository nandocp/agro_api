from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator

from app.domain.accounts.enums import AccountPlan
from app.shared.schemas import BaseSchema, Pagination
from app.shared.utils import digits_only


class AccountFilters(Pagination):
    plan: AccountPlan | None = Field(None)
    name: str | None = Field(None, max_length=255)
    document: str | None = Field(None)
    archived: bool | None = Field(None)


class AccountCreate(BaseModel):
    name: str
    document: str
    plan: AccountPlan = AccountPlan.FREE

    @field_validator('document')
    @classmethod
    def normalize_document(cls, v: str) -> str:
        return digits_only(v)


class AccountResponse(BaseSchema):
    name: str
    document: str
    plan: str
    archived_at: datetime | None

    @field_serializer('document')
    def mask_document(value: str) -> str:
        doc = {'cpf': 11, 'cnpj': 14}
        if len(value) == doc['cpf']:
            return f'{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}'
        if len(value) == doc['cnpj']:
            return (
                f'{value[:2]}.'
                f'{value[2:5]}.'
                f'{value[5:8]}/'
                f'{value[8:12]}-'
                f'{value[12:]}'
            )
        return value


class AccountUpdatePlan(BaseModel):
    plan: AccountPlan
