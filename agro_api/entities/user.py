from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Set

from sqlalchemy import Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from agro_api.entities.base import table_registry

if TYPE_CHECKING:
    from agro_api.entities.estate import Estate


class UserRole(str, Enum):
    agro_user = 'agro_user'
    agro_admin = 'agro_admin'
    estate_user = 'estate_user'
    estate_coord = 'estate_coord'
    estate_admin = 'estate_admin'


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

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

    estates: Mapped[Set['Estate']] = relationship(
        back_populate='user',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin'
    )
