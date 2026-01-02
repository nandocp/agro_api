from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from .base import table_registry


class EstateKind(Enum):
    RURAL = 'rural'
    INTRAURBAN = 'intraurban'
    PERIURBAN = 'periurban'


@mapped_as_dataclass(table_registry)
class Estate:
    __tablename__ = 'estates'

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
    )

    user_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))

    label: Mapped[str] = mapped_column(unique=False)

    slug: Mapped[str] = mapped_column(unique=True, nullable=False)

    opened_at: Mapped[datetime] = mapped_column(
        nullable=True,
        server_default=func.now()
    )

    closed_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    kind: Mapped[EstateKind] = mapped_column(default=EstateKind('rural'))

    def is_urban(self):
        'urban' in self.kind
