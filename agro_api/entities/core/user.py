from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.activity import Activity
    from agro_api.entities.core import Account


class UserRole(str, Enum):
    AGRO_USER = 'agro_user'
    AGRO_ADMIN = 'agro_admin'
    ESTATE_USER = 'estate_user'
    ESTATE_COORD = 'estate_coord'
    ESTATE_ADMIN = 'estate_admin'


@mapped_as_dataclass(table_registry)
class User(BaseEntity):
    __tablename__ = 'users'

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
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    account: Mapped['Account'] = relationship(back_populates='users')

    created_activities: Mapped[List['Activity']] = relationship(
        init=False, back_populates='creator'
    )

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'
