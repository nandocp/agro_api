from pydantic import BaseModel, field_validator


class AccountCreate(BaseModel):
    name: str
    document: str

    @field_validator('document')
    @classmethod
    def normalize_document(cls, v: str) -> str:
        return ''.join(filter(str.isdigit, v))
