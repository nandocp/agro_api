# import uuid
from datetime import datetime

from sqlalchemy import Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from .base import table_registry


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

    username: Mapped[str] = mapped_column(unique=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password: Mapped[str] = mapped_column()

    is_active: Mapped[bool] = mapped_column(
        init=False, default=True
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
    deleted_at: Mapped[datetime] = mapped_column(
        init=False,
        nullable=True
    )

    # def __repr__(self):
    #     return f'{self.email}'
