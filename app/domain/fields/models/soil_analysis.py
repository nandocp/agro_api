from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.model import BaseModel

if TYPE_CHECKING:
    from app.domain.fields.models import Field


class FieldSoilAnalysis(BaseModel):
    __tablename__ = 'field_soil_analyses'
    __table_args__ = (
        CheckConstraint(
            'sampling_depth_cm > 0', name='ck_dsampling_epth_positive'
        ),
        CheckConstraint(
            'ph_h2o IS NULL OR (ph_h2o >= 0 AND ph_h2o <= 14)',
            name='ck_ph_h2o_range',
        ),
        CheckConstraint(
            'analyzed_at IS NULL OR analyzed_at >= collected_at',
            name='ck_analysis_date_after_collection',
        ),
    )

    field_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey('fields.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )

    collected_at: Mapped[date] = mapped_column(
        Date, nullable=False, index=True
    )
    analyzed_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment='Date laboratory issued the results',
    )

    sampling_depth_cm: Mapped[int | None] = mapped_column(
        Integer,
        nullable=False,
        default=None,
        comment='Sampling depth in centimeters. Typically 0-20cm or 20-40cm',
    )

    ph_h2o: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), default=None, nullable=True, comment='pH em água (0-14)'
    )
    base_saturation_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), default=None, nullable=True
    )
    organic_matter_g_dm3: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), default=None, nullable=True
    )
    texture_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment='Textural classification. Ex: clayey, medium, sandy, etc',
    )

    chemical: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
        comment=(
            'Chemical characteristics: '
            'ph, organic_matter, macro and micronutrients'
        ),
    )
    physical: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
        comment=(
            'Physical characteristics: '
            'texture, density, porosity, water retention'
        ),
    )
    biological: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
        comment=(
            'Biological characteristics: '
            'microbial biomass, respiration, nitrogen'
        ),
    )

    collector_name: Mapped[str] = mapped_column(String(255), nullable=False)
    collector_registry: Mapped[str] = mapped_column(String(64), nullable=False)
    laboratory_name: Mapped[str] = mapped_column(String(255), nullable=False)
    laboratory_protocol: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        default=None,
        comment='Laboratory report or protocol number',
    )

    # ========== Field observations ==========
    # implementar journal entry
    # notes: Mapped[str | None] = mapped_column(
    #     Text, comment='Observações gerais sobre a análise'
    # )

    # ========== Relationships ==========
    field: Mapped['Field'] = relationship(
        back_populates='soil_analyses', lazy='raise', init=False
    )

    def __repr__(self):
        return (
            f'SoilAnalysis(field={self.field_id}, date={self.sampling_date})'
        )
