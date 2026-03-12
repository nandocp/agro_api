from datetime import datetime
from enum import Enum

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from agro_api.entities.base import BaseEntity
from config.database import table_registry


class ProtectionType(str, Enum):
    LEGAL_RESERVE = 'legal_reserve'
    CONSERVATION = 'conservation'
    HISTORIC = 'historic'
    CONTRACT = 'contract'


@mapped_as_dataclass(table_registry)
class FieldProtection(BaseEntity):
    __tablename__ = 'field_protections'
    __table_args__ = (
        UniqueConstraint(
            'field_id', 'protection_type', name='idx_field_protection'
        ),
    )

    field_id: Mapped[Uuid] = mapped_column(ForeignKey('fields.id'))
    created_by_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))

    protection_type: Mapped[ProtectionType]
    reason: Mapped[str | None] = mapped_column(String(256))

    expires_at: Mapped[datetime | None]
    started_at: Mapped[datetime] = mapped_column(default=func.now())

    # What operations are restricted
    blocks_deletion: Mapped[bool] = mapped_column(default=True)
    blocks_transition: Mapped[bool] = mapped_column(default=True)
    blocks_boundary_change: Mapped[bool] = mapped_column(default=False)
