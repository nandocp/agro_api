from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.core import Account


class UserRole(str, Enum):
    AGRO_USER = 'agro_user'
    AGRO_ADMIN = 'agro_admin'
    ESTATE_USER = 'estate_user'
    ESTATE_COORD = 'estate_coord'
    ESTATE_ADMIN = 'estate_admin'


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.uuidv7(),
        nullable=False,
    )

    account_id: Mapped[Uuid] = mapped_column(ForeignKey('accounts.id'))

    name: Mapped[str] = mapped_column(unique=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password: Mapped[str] = mapped_column()

    is_active: Mapped[bool] = mapped_column(init=False, default=True)

    jti: Mapped[Uuid] = mapped_column(
        UUID, init=False, nullable=True, unique=True
    )

    current_sign_in_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    last_sign_in_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    account: Mapped['Account'] = relationship(back_populates='users')

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
