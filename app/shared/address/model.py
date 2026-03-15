from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.model import BaseModel


class Address(BaseModel):
    __tablename__ = 'addresses'

    street: Mapped[str | None] = mapped_column(
        String(200), default=None, nullable=True
    )
    number: Mapped[str | None] = mapped_column(
        String(20), default=None, nullable=True
    )
    complement: Mapped[str | None] = mapped_column(
        String(100), default=None, nullable=True
    )
    neighborhood: Mapped[str | None] = mapped_column(
        String(100), default=None, nullable=True
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(8), nullable=False)
    country: Mapped[str] = mapped_column(String(2), default='BR')
    postal_code: Mapped[str | None] = mapped_column(
        String(10), default=None, nullable=True
    )
    reference: Mapped[str | None] = mapped_column(
        String(300),
        default=None,
        nullable=True,
        comment='Reference — Km marker, road name, landmark',
    )
