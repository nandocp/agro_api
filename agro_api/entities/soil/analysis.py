from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from agro_api.entities.base import BaseEntity
from config.database import table_registry

if TYPE_CHECKING:
    from agro_api.entities.field import Field


@table_registry.mapped_as_dataclass(kw_only=True)
class SoilAnalysis(BaseEntity):
    __tablename__ = 'soil_analyses'
    __table_args__ = (
        CheckConstraint('sampling_depth_cm > 0', name='ck_depth_positive'),
        CheckConstraint(
            'ph IS NULL OR (ph >= 0 AND ph <= 14)', name='ck_ph_range'
        ),
        CheckConstraint('organic_matter_percent >= 0', name='ck_om_positive'),
    )

    field_id: Mapped[Uuid] = mapped_column(
        ForeignKey('fields.id', ondelete='CASCADE'), nullable=False, index=True
    )

    # Data da coleta (diferente de created_at)
    sampling_date: Mapped[date] = mapped_column(nullable=False, index=True)

    # Profundidade da amostra (ex: 0-20 cm)
    sampling_depth_cm: Mapped[int] = mapped_column(nullable=False)

    # ========== CARACTERÍSTICAS QUÍMICAS ==========
    ph: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), comment='pH em água (0-14)'
    )

    organic_matter_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    phosphorus_mg_dm3: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    potassium_mmol_dm3: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    calcium_mmol_dm3: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    magnesium_mmol_dm3: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    aluminum_mmol_dm3: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    cation_exchange_capacity: Mapped[Decimal | None] = mapped_column(
        Numeric(7, 2)
    )

    base_saturation_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    # ========== Physical characteristics ==========
    clay_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))

    silt_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))

    sand_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))

    bulk_density_g_cm3: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))

    field_capacity_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    wilting_point_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    available_water_mm: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))

    collector_name: Mapped[str]
    collector_registry: Mapped[str]
    laboratory: Mapped[str]

    # ========== Field observations ==========
    notes: Mapped[str | None] = mapped_column(
        Text, comment='Observações gerais sobre a análise'
    )

    # ========== Relationships ==========
    field: Mapped['Field'] = relationship(back_populates='soil_analyses')

    def __repr__(self):
        return (
            f'SoilAnalysis(field={self.field_id}, date={self.sampling_date})'
        )


# patricia vaz
# fernando rebelo
