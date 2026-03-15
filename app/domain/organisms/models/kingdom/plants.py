from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..organism import Organism


class Plant(Organism):
    __tablename__ = 'plants'
    __mapper_args__ = {'polymorphic_identity': 'plant'}
    __table_args__ = (
        CheckConstraint(
            'soil_ph_min IS NULL OR (soil_ph_min >= 0 AND soil_ph_min <= 14)',
            name='ck_plant_ph_min_range',
        ),
        CheckConstraint(
            'soil_ph_max IS NULL OR (soil_ph_max >= 0 AND soil_ph_max <= 14)',
            name='ck_plant_ph_max_range',
        ),
        CheckConstraint(
            (
                'soil_ph_min IS NULL OR '
                'soil_ph_max IS NULL OR '
                'soil_ph_max >= soil_ph_min'
            ),
            name='ck_plant_ph_order',
        ),
        CheckConstraint(
            (
                'min_temperature_c IS NULL OR '
                'max_temperature_c IS NULL OR '
                'max_temperature_c >= min_temperature_c'
            ),
            name='ck_plant_temperature_order',
        ),
        CheckConstraint(
            (
                'recommended_altitude_min_m IS NULL OR '
                'recommended_altitude_max_m IS NULL OR '
                'recommended_altitude_max_m >= recommended_altitude_min_m'
            ),
            name='ck_plant_altitude_order',
        ),
    )

    id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    plant_cycle: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )
    growth_habit: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )
    primary_use: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )
    secondary_uses: Mapped[List[str] | None] = mapped_column(
        ARRAY(String(50)), nullable=True, default=None
    )
    max_height_cm: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )
    min_temperature_c: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), nullable=True, default=None
    )
    max_temperature_c: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), nullable=True, default=None
    )
    water_requirement: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )
    days_to_maturity: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )
    days_to_germination: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )
    drought_tolerance: Mapped[str | None] = mapped_column(
        String(32), default=None, nullable=True
    )
    frost_tolerance: Mapped[str | None] = mapped_column(
        String(32), default=None, nullable=True
    )
    flood_tolerance: Mapped[str | None] = mapped_column(
        String(32), default=None, nullable=True
    )
    soil_ph_min: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), nullable=True, default=None
    )
    soil_ph_max: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), nullable=True, default=None
    )
    recommended_altitude_min_m: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True, default=None
    )
    recommended_altitude_max_m: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True, default=None
    )
    nitrogen_fixing: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment='Fixes atmospheric nitrogen (legumes)',
    )
    allelopathic: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment='Suppresses growth of other plants',
    )
