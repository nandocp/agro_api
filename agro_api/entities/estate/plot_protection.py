from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from agro_api.entities.core import User


class ProtectionType(str, Enum):
    LEGAL_RESERVE = 'legal_reserve'
    CONSERVATION = 'conservation'
    HISTORIC = 'historic'
    CONTRACT = 'contract'


class PlotProtection:
    __tablename__ = 'plot_protections'
    __table_args__ = (
        UniqueConstraint('plot_id', 'protection_type', name='idx_plot_protection')
    )

    id: Mapped[Uuid] = mapped_column(
        UUID,
        init=False,
        primary_key=True,
        server_default=func.uuidv7(),
        nullable=False,
    )
    plot_id: Mapped[Uuid] = mapped_column(ForeignKey('estate_plots.id'))
    # Who created the protection
    created_by_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))

    protection_type: Mapped[ProtectionType]
    reason: Mapped[str | None] = mapped_column(String(256))

    started_at: Mapped[datetime] = mapped_column(default=func.now())
    expires_at: Mapped[datetime | None]

    # Timestamps metadata
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    # What operations are restricted
    blocks_deletion: Mapped[bool] = mapped_column(default=True)
    blocks_transition: Mapped[bool] = mapped_column(default=True)
    blocks_boundary_change: Mapped[bool] = mapped_column(default=False)
