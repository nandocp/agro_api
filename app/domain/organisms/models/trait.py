from __future__ import annotations

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.model import BaseModel


class OrganismTrait(BaseModel):
    __tablename__ = 'organism_traits'

    __table_args__ = (UniqueConstraint('name', name='uq_organism_trait_name'),)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)


# from sqlalchemy import Table, Column, ForeignKey
# from app.shared.model import DeclarativeModel
# PlantingCompositionTrait = Table(
#     'planting_composition_traits',
#     DeclarativeModel.metadata,
#     Column(
#         'composition_id',
#         ForeignKey('planting_compositions.id', ondelete='CASCADE'),
#         primary_key=True,
#     ),
#     Column(
#         'trait_id',
#         ForeignKey('organism_traits.id', ondelete='RESTRICT'),
#         primary_key=True,
#     ),
# )
