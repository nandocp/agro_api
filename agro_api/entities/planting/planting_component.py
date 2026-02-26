class PlantingComponent(Base):
    """A single component within a planting system."""
    __tablename__ = 'planting_components'

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    planting_id: Mapped[Uuid] = mapped_column(ForeignKey('plantings.id'))

    # What was planted
    species_id: Mapped[Uuid] = mapped_column(ForeignKey('plant_species.id'))
    variety: Mapped[str | None]

    # How it was planted
    density_per_ha: Mapped[int]  # plants per hectare
    spatial_arrangement: Mapped[str]  # "row", "scattered", "cluster"
    row_spacing_m: Mapped[float | None]
    plant_spacing_m: Mapped[float | None]

    # Which stratum (for agroforestry)
    stratum: Mapped[Stratum | None]  # canopy, midstory, understory, ground

    # Commercial info
    primary_purpose: Mapped[Purpose]  # timber, fruit, crop, fodder, shade
    is_commodity: Mapped[bool] = mapped_column(default=False)  # soy, corn vs specialty

    # Expected products
    expected_yield_kg_ha: Mapped[float | None]
    actual_yield_kg_ha: Mapped[float | None]
