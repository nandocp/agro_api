https://medium.com/@notarious2/working-with-spatial-data-using-fastapi-and-geoalchemy-797d414d2fe7

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

# ============================================================================
# SLOPE CLASS
# ============================================================================
@table_registry.mapped_as_dataclass(kw_only=True)
class SlopeClass(BaseEntity):
    """Classificação de declividade do terreno (i18n ready)."""
    __tablename__ = 'slope_classes'

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        comment="Código interno: 'flat', 'gentle', 'moderate', 'strong', 'steep'"
    )

    min_slope: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        comment="Declividade mínima em percentual (opcional)"
    )
    max_slope: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        comment="Declividade máxima em percentual (opcional)"
    )

    # Relacionamento com traduções
    translations: Mapped[List['SlopeClassTranslation']] = relationship(
        back_populates='slope_class',
        cascade='all, delete-orphan'
    )

    __table_args__ = (
        CheckConstraint('min_slope IS NULL OR min_slope >= 0'),
        CheckConstraint('max_slope IS NULL OR max_slope <= 100'),
        CheckConstraint(
            '(min_slope IS NULL AND max_slope IS NULL) OR min_slope <= max_slope',
            name='ck_slope_range'
        ),
    )


@table_registry.mapped_as_dataclass(kw_only=True)
class SlopeClassTranslation(BaseEntity):
    """Traduções das classes de declividade."""
    __tablename__ = 'slope_class_translations'
    __table_args__ = (
        UniqueConstraint('slope_class_id', 'locale', name='uq_slope_class_locale'),
    )

    slope_class_id: Mapped[Uuid] = mapped_column(
        ForeignKey('slope_classes.id', ondelete='CASCADE'),
        nullable=False
    )
    locale: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Código do idioma: 'pt-BR', 'en-US', 'es'"
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nome traduzido: 'Plano', 'Ondulado', 'Montanhoso'"
    )
    description: Mapped[str | None] = mapped_column(
        String(200),
        comment="Descrição traduzida (opcional)"
    )

    # Relacionamento
    slope_class: Mapped['SlopeClass'] = relationship(back_populates='translations')

    slope_classes = [
        {
            'code': 'flat',
            'min_slope': 0,
            'max_slope': 3,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Plano', 'description': '0-3% declividade'},
                {'locale': 'en-US', 'display_name': 'Flat', 'description': '0-3% slope'},
                {'locale': 'es', 'display_name': 'Plano', 'description': '0-3% pendiente'},
            ]
        },
        {
            'code': 'gentle',
            'min_slope': 3,
            'max_slope': 8,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Suave Ondulado', 'description': '3-8% declividade'},
                {'locale': 'en-US', 'display_name': 'Gently Sloping', 'description': '3-8% slope'},
                {'locale': 'es', 'display_name': 'Suavemente Ondulado', 'description': '3-8% pendiente'},
            ]
        },
        {
            'code': 'moderate',
            'min_slope': 8,
            'max_slope': 20,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Ondulado', 'description': '8-20% declividade'},
                {'locale': 'en-US', 'display_name': 'Moderately Sloping', 'description': '8-20% slope'},
                {'locale': 'es', 'display_name': 'Ondulado', 'description': '8-20% pendiente'},
            ]
        },
        {
            'code': 'strong',
            'min_slope': 20,
            'max_slope': 45,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Forte Ondulado', 'description': '20-45% declividade'},
                {'locale': 'en-US', 'display_name': 'Strongly Sloping', 'description': '20-45% slope'},
                {'locale': 'es', 'display_name': 'Fuertemente Ondulado', 'description': '20-45% pendiente'},
            ]
        },
        {
            'code': 'steep',
            'min_slope': 45,
            'max_slope': 100,
            'translations': [
                {'locale': 'pt-BR', 'display_name': 'Montanhoso', 'description': '>45% declividade'},
                {'locale': 'en-US', 'display_name': 'Steep', 'description': '>45% slope'},
                {'locale': 'es', 'display_name': 'Escarpado', 'description': '>45% pendiente'},
            ]
        },
    ]
