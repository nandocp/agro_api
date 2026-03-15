from __future__ import annotations

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.model import BaseModel


class OrganismCommonName(BaseModel):
    __tablename__ = 'plant_common_names'
    __table_args__ = (
        UniqueConstraint(
            'organism_id', 'name', 'language', name='uq_organism_name_lang'
        ),
        Index('idx_common_name_search', 'name'),
    )

    organism_id: Mapped[Uuid] = mapped_column(ForeignKey('plant_species.id'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str | None] = mapped_column(
        String(64), nullable=True, default=None
    )
    language: Mapped[str] = mapped_column(
        String(10), default='pt-BR', nullable=False
    )
    is_preferred: Mapped[bool] = mapped_column(
        default=False,
        comment='Preferred name for display in this language/region',
    )
