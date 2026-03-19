from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from config.database import table_registry

from ..planting import Planting


@table_registry.mapped_as_dataclass(kw_only=True)
class BedPlanting(Planting):
    __tablename__ = 'pit_plantings'
    __mapper_args__ = {'polymorphic_identity': 'bed_planting'}
    __table_args__ = (
        CheckConstraint('row_spacing_cm > 0'),
        CheckConstraint('bed_spacing_cm > 0'),
    )

    id: Mapped[Uuid] = mapped_column(
        ForeignKey('plantings.id'), primary_key=True, nullable=False
    )

    row_spacing_cm: Mapped[int] = mapped_column(Integer, nullable=False)
    bed_spacing_cm: Mapped[int] = mapped_column(Integer, nullable=False)
    seeds_per_bed: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )
