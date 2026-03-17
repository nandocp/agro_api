from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from config.database import table_registry

from ..planting import Planting


@table_registry.mapped_as_dataclass(kw_only=True)
class BroadcastPlanting(Planting):
    __tablename__ = 'broadcast_plantings'
    __mapper_args__ = {'polymorphic_identity': 'broadcast_planting'}

    id: Mapped[Uuid] = mapped_column(
        ForeignKey('plantings.id'), primary_key=True
    )

    total_seeding_rate_kg_ha: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2)
    )
