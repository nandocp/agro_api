# app/shared/address/schemas.py
from pydantic import BaseModel

from app.shared.schemas import BaseSchema


class AddressCreate(BaseModel):
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    city: str
    state: str
    country: str = 'BR'
    postal_code: str | None = None
    reference: str | None = None


class AddressUpdate(AddressCreate):
    city: str | None = None
    state: str | None = None
    country: str | None = None


class AddressResponse(BaseSchema):
    street: str | None
    number: str | None
    complement: str | None
    neighborhood: str | None
    city: str
    state: str
    country: str
    postal_code: str | None
    reference: str | None
