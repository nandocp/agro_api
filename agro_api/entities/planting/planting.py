
class Planting(Base):
    """A planting event or system."""
    __tablename__ = 'plantings'

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    plot_id: Mapped[Uuid] = mapped_column(ForeignKey('estate_plots.id'))

    # What kind of system
    planting_system: Mapped[PlantingSystem]

    # When
    planting_date: Mapped[date]
    status: Mapped[PlantingStatus]

    # Components (the actual plants)
    components: Mapped[List['PlantingComponent']] = relationship(
        cascade='all, delete-orphan'
    )

    # Design metadata
    design_name: Mapped[str | None]  # "Taungya System", "Alley Cropping"
    total_area_m2: Mapped[Decimal | None]  # if different from plot
    notes: Mapped[str | None]
