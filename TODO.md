class Address:
    __tablename__ = 'addresses'

    id: Mapped[Uuid] = mapped_column(primary_key=True, server_default=func.uuidv7())

    # Core address fields
    street: Mapped[str | None]
    number: Mapped[str | None]  # String to handle "S/N", "Km 12", etc.
    complement: Mapped[str | None]
    neighborhood: Mapped[str | None]
    city: Mapped[str]
    state: Mapped[str]  # Could be FK to states table
    postal_code: Mapped[str | None]
    country: Mapped[str] = mapped_column(default='BR')

    # Optional geocoding fields
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    geocoding_accuracy: Mapped[str | None]  # rooftop, street, approximate, etc.

    # Metadata
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    estate: Mapped['Estate'] = relationship(back_populates='address')

-------------------------------------------------------------------------------------------------
PLOT: add soil_type
-------------------------------------------------------------------------------------------------
# ============================================================================
# TAG (master table)
# ============================================================================

class Tag(BaseEntity):
    """A reusable tag that can be applied to various entities."""
    __tablename__ = 'tags'

    # Core fields
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="Tag name, automatically lowercased and normalized"
    )
    display_name: Mapped[str | None] = mapped_column(
        String(50),
        comment="Display version with proper capitalization (e.g., 'Pest Control')"
    )

    # Optional metadata
    color: Mapped[str | None] = mapped_column(
        String(7),
        comment="Hex color code (e.g., '#FF5733') for UI display"
    )
    description: Mapped[str | None] = mapped_column(
        String(200),
        comment="What this tag means and when to use it"
    )

    # Categorization
    category: Mapped[TagCategory | None] = mapped_column(
        comment="High-level grouping: 'issue', 'crop', 'location', 'activity'"
    )

    # Who created it (for governance)
    created_by_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )

    # Usage tracking (can be updated periodically)
    usage_count: Mapped[int] = mapped_column(default=0)
    last_used_at: Mapped[datetime | None]

    # For tag hierarchies (parent-child relationships)
    parent_tag_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('tags.id', ondelete='SET NULL'),
        comment="For hierarchical tags: 'pest' → 'coffee-borer'"
    )

    # Relationships
    created_by: Mapped['User'] = relationship(foreign_keys=[created_by_id])
    parent_tag: Mapped['Tag'] = relationship(remote_side='Tag.id')
    child_tags: Mapped[List['Tag']] = relationship(
        back_populates='parent_tag',
        cascade='all, delete-orphan'
    )

    @validates('name')
    def normalize_name(self, key, value):
        """Ensure tag names are always stored lowercase."""
        return value.lower().strip()

    def __repr__(self):
        return f"Tag(name={self.name})"


# ============================================================================
# TAGGING (polymorphic junction table)
# ============================================================================

class Tagging(BaseEntity):
    """Links tags to any entity in the system."""
    __tablename__ = 'taggings'

    tag_id: Mapped[Uuid] = mapped_column(
        ForeignKey('tags.id', ondelete='CASCADE'),
        primary_key=True
    )

    # Polymorphic association: can tag any entity
    entity_type: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        comment="Table name: 'journal_entries', 'tasks', 'plant_species'"
    )
    entity_id: Mapped[Uuid] = mapped_column(
        primary_key=True,
        comment="ID of the tagged entity"
    )

    # Who applied this tag
    tagged_by_id: Mapped[Uuid | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )
    tagged_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    # Optional context (why this tag was applied)
    context: Mapped[str | None] = mapped_column(
        String(200),
        comment="e.g., 'observed during morning inspection'"
    )

    # Relationships
    tag: Mapped['Tag'] = relationship()
    tagged_by: Mapped['User'] = relationship()

    __table_args__ = (
        Index('ix_taggings_entity', 'entity_type', 'entity_id'),
    )

    def __repr__(self):
        return f"Tagging(tag={self.tag_id}, {self.entity_type}:{self.entity_id})"


# ============================================================================
# TAG CATEGORY ENUM
# ============================================================================

class TagCategory(str, Enum):
    ISSUE = 'issue'              # pest, disease, problem
    CROP = 'crop'                # coffee, corn, timber
    LOCATION = 'location'        # north-block, greenhouse, field-a
    ACTIVITY = 'activity'        # pruning, harvesting, irrigation
    STATUS = 'status'            # urgent, completed, pending
    QUALITY = 'quality'          # organic, premium, grade-a
    WEATHER = 'weather'          # frost, drought, rain
    EQUIPMENT = 'equipment'      # tractor, irrigator, sprayer
    CUSTOM = 'custom'            # user-defined
-------------------------------------------------------------------------------------------------
