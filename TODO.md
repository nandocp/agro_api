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

===========================================================================================
PROVENANCE - origem verificável
===========================================================================================
class EstateEvent(ModelBase): <=== USAR ESSA
    __tablename__ = 'estate_events'
    __table_args__ = (
        Index('ix_estate_events_source', 'estate_id', 'source'),
        Index('ix_estate_events_action', 'estate_id', 'source', 'action'),
    )

    estate_id: Mapped[UUID] = mapped_column(
        ForeignKey('estates.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    source: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment='registry, field, activity, estate'
    )
    action: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment='submitted, approved, divided, merged, archived...'
    )
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )

    estate: Mapped['Estate'] = relationship(lazy='raise', init=False)
    creator: Mapped['User'] = relationship(lazy='raise', init=False)
# app/domain/activities/models/event.py
class ActivityEvent(ORMBase):
    __tablename__ = 'activity_events'

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    activity_id: Mapped[UUID] = mapped_column(
        ForeignKey('activities.id'), nullable=False, index=True
    )
    document_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('activity_documents.id'), nullable=True,
        comment='Populated when event is related to a document'
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )

    activity: Mapped['Activity'] = relationship(lazy='raise', init=False)
    document: Mapped['ActivityDocument | None'] = relationship(
        lazy='raise', init=False
    )

# app/domain/activities/services/event.py
def compute_hash(previous_hash: str, payload: dict, timestamp: datetime) -> str:
    content = f'{previous_hash}{json.dumps(payload, sort_keys=True)}{timestamp.isoformat()}'
    return sha256(content.encode()).hexdigest()

# app/shared/event_bus.py ==> quem vai criar os events com toda a lógica
from hashlib import sha256
from uuid import UUID
import json
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.events import DomainEvent
from app.domain.activities.models.event import ActivityEvent


class EventBus:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, event: DomainEvent) -> ActivityEvent:
        previous_hash = await self._get_previous_hash(event.activity_id)
        hash_value = self._compute_hash(
            previous_hash,
            event.payload,
            event.occurred_at,
        )

        record = ActivityEvent(
            id=event.id,
            activity_id=event.activity_id,
            event_type=event.event_type,
            payload=event.payload,
            previous_hash=previous_hash,
            hash=hash_value,
            created_at=event.occurred_at,
            created_by=event.created_by,
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def _get_previous_hash(self, activity_id: UUID) -> str:
        result = await self._session.scalar(
            select(ActivityEvent.hash)
            .where(ActivityEvent.activity_id == activity_id)
            .order_by(ActivityEvent.created_at.desc())
            .limit(1)
        )
        return result or '0' * 64

    @staticmethod
    def _compute_hash(
        previous_hash: str,
        payload: dict,
        timestamp: datetime,
    ) -> str:
        content = (
            f'{previous_hash}'
            f'{json.dumps(payload, sort_keys=True)}'
            f'{timestamp.isoformat()}'
        )
        return sha256(content.encode()).hexdigest()
# app/shared/service.py
class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self._session = session
        self.repo = CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType](
            model, session
        )
        self.events = EventBus(session)
# app/domain/activities/event_creator.py
from uuid import UUID
from app.domain.activities.models.activity import Activity
from app.domain.activities.models.document import ActivityDocument
from app.domain.activities.events import (
    ActivityStartedEvent,
    ActivityCompletedEvent,
    ActivityCancelledEvent,
    DocumentIssuedEvent,
    PlantingRegisteredEvent,
)
from app.domain.activities.planting.models.planting import Planting
from app.shared.events import DomainEvent


class ActivityEventCreator:

    @staticmethod
    def activity_started(activity: Activity, created_by: UUID) -> DomainEvent:
        return ActivityStartedEvent(
            activity_id=activity.id,
            payload={
                'status': activity.status,
                'started_at': activity.started_at.isoformat(),
                'field_id': str(activity.field_id),
            },
            created_by=created_by,
        )

    @staticmethod
    def activity_completed(activity: Activity, created_by: UUID) -> DomainEvent:
        return ActivityCompletedEvent(
            activity_id=activity.id,
            payload={
                'status': activity.status,
                'finished_at': activity.finished_at.isoformat(),
                'total_area_m2': str(activity.total_area_m2),
            },
            created_by=created_by,
        )

    @staticmethod
    def activity_cancelled(activity: Activity, created_by: UUID) -> DomainEvent:
        return ActivityCancelledEvent(
            activity_id=activity.id,
            payload={
                'status': activity.status,
                'cancelled_at': activity.finished_at.isoformat(),
                'notes': activity.notes,
            },
            created_by=created_by,
        )

    @staticmethod
    def document_issued(
        activity_id: UUID,
        document: ActivityDocument,
        created_by: UUID,
    ) -> DomainEvent:
        return DocumentIssuedEvent(
            activity_id=activity_id,
            payload={
                'document_id': str(document.id),
                'document_type': document.document_type,
                'protocol': document.protocol,
                'issuer': document.issuer,
                'issued_at': document.issued_at.isoformat() if document.issued_at else None,
                'valid_until': document.valid_until.isoformat() if document.valid_until else None,
            },
            created_by=created_by,
        )

    @staticmethod
    def planting_registered(
        activity_id: UUID,
        planting: Planting,
        created_by: UUID,
    ) -> DomainEvent:
        return PlantingRegisteredEvent(
            activity_id=activity_id,
            payload={
                'planting_id': str(planting.id),
                'arrangement_type': planting.arrangement_type,
                'culture_type': planting.culture_type,
                'total_area_m2': str(planting.total_area_m2) if planting.total_area_m2 else None,
            },
            created_by=created_by,
        )


# app/domain/activities/models/document.py
class ActivityDocument(ModelBase):
    __tablename__ = 'activity_documents'
    __table_args__ = (
        CheckConstraint(
            'length(trim(protocol)) > 0',
            name='ck_document_protocol_not_empty'
        ),
    )

    activity_id: Mapped[UUID] = mapped_column(
        ForeignKey('activities.id'), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment='Validated by API layer — see DocumentType enum'
    )
    protocol: Mapped[str] = mapped_column(
        String(128), nullable=False,
        comment='Identifier issued by the competent authority'
    )
    issuer: Mapped[str] = mapped_column(
        String(128), nullable=False,
        comment='Authority or entity that issued the document'
    )
    issued_at: Mapped[date | None] = mapped_column(default=None)
    valid_until: Mapped[date | None] = mapped_column(default=None)
    status: Mapped[DocumentStatus] = mapped_column(
        default=DocumentStatus.PENDING, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String(500), default=None)

    activity: Mapped['Activity'] = relationship(
        back_populates='documents', lazy='raise', init=False
    )
    events: Mapped[list['ActivityEvent']] = relationship(
        back_populates='document', lazy='raise', init=False
    )

NÍVEIS PARA PROTEÇÃO DE EVENTOS
nivel 1: Permissões no PostgreSQL
-- usuário da aplicação não tem UPDATE nem DELETE na tabela de eventos
REVOKE UPDATE, DELETE ON activity_events FROM agro_app_user;

-- só INSERT permitido
GRANT INSERT, SELECT ON activity_events TO agro_app_user;
-------------------------------
nivel 2: Trigger no PostgreSQL
CREATE OR REPLACE FUNCTION prevent_event_modification()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Activity events are immutable';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER immutable_activity_events
    BEFORE UPDATE OR DELETE ON activity_events
    FOR EACH ROW
    EXECUTE FUNCTION prevent_event_modification();
-------------------------------
nivel 3: Hash encadeado para detecção de adulteração
async def verify_chain_integrity(
    session: AsyncSession,
    estate_id: UUID
) -> bool:
    events = await session.execute(
        select(ActivityEvent)
        .where(ActivityEvent.estate_id == estate_id)
        .order_by(ActivityEvent.created_at)
    )
    previous_hash = '0' * 64  # genesis hash

    for event in events.scalars():
        expected_hash = compute_hash(
            previous_hash,
            event.payload,
            event.created_at
        )
        if event.hash != expected_hash:
            return False  # adulteração detectada
        previous_hash = event.hash

    return True
-------------------------------
===========================================================================================
ARCH
===========================================================================================
bapp/
├── app/
│   ├── domain/
│   │   ├── accounts/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── account.py
│   │   │   │   └── address.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── auth.py
│   │   ├── estate/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── estate.py
│   │   │   │   └── registry.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── field/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── field.py
│   │   │   │   ├── protection.py
│   │   │   │   ├── transition.py
│   │   │   │   └── soil/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── analysis.py
│   │   │   │       └── classification.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── plant/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── species.py
│   │   │   │   ├── common_name.py
│   │   │   │   ├── synonym.py
│   │   │   │   └── trait.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   └── activity/
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   └── activity.py
│   │       ├── planting/
│   │       │   ├── models/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── planting.py
│   │       │   │   ├── composition.py
│   │       │   │   └── methods/
│   │       │   │       ├── __init__.py
│   │       │   │       ├── row.py
│   │       │   │       ├── bed.py
│   │       │   │       └── broadcast.py
│   │       │   ├── schemas.py
│   │       │   ├── service.py
│   │       │   └── repository.py
│   │       ├── task/
│   │       │   ├── models/
│   │       │   │   ├── __init__.py
│   │       │   │   └── task.py
│   │       │   ├── schemas.py
│   │       │   ├── service.py
│   │       │   └── repository.py
│   │       ├── journal/
│   │       │   ├── models/
│   │       │   │   ├── __init__.py
│   │       │   │   └── entry.py
│   │       │   ├── schemas.py
│   │       │   └── repository.py
│   │       ├── schemas.py
│   │       ├── service.py
│   │       └── repository.py
│   ├── shared/
│   │   ├── base.py             # BaseEntity, table_registry
│   │   ├── repository.py       # BaseRepository genérico
│   │   └── utils.py            # relationship wrapper
│   └── main.py
├── config/
│   ├── settings.py
│   ├── database.py
│   ├── logging.py
│   └── http_misc.py
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── seeds/
│   ├── production/
│   │   └── required_data.py
│   └── development/
│       └── fixtures.py
└── toolbox/
```

---

**Quando chegar nos endpoints, a camada `api/` entra dentro de `app/`:**
```
app/
├── api/
│   ├── v1/
│   │   ├── router.py           # agrega todos os routers
│   │   ├── accounts.py
│   │   ├── estate.py
│   │   ├── fields.py
│   │   ├── plants.py
│   │   └── activities/
│   │       ├── router.py
│   │       ├── planting.py
│   │       ├── task.py
│   │       └── journal.py
│   └── middleware.py
├── domain/
├── shared/
└── main.py


""" drainage = CLASSES DE DRENAGEM
Excessivamente drenado – água removida muito rapidamente
Fortemente drenado – água removida rapidamente (<18g/100g)
Acentuadamente drenado – água removida rapidamente (>18g/100g)
Bem drenado – água removida com facilidade, porém não rapidamente
Moderadamente drenado – água removida lentamente
Imperfeitamente drenado – solo permanece molhado
Mal drenado – solo permanece molhado muito tempo
Muito mal drenado – solo permanentemente encharcado

Excessively Drained
Water is removed very rapidly. The occurrence of internal free water commonly
is very rare or very deep. The soils are commonly coarse-textured and have very
Document last revised April 2010
2 Connecticut Environmental Conditions Online – www.cteco.uconn.edu
high hydraulic conductivity or are very shallow.
Somewhat Excessively Drained
Water is removed from the soil rapidly. Internal free water occurrence
commonly is very rare or very deep. The soils are commonly coarse-textured
and have high saturated hydraulic conductivity or are very shallow.
Well Drained
Water is removed from the soil readily but not rapidly. Internal free water
occurrence commonly is deep or very deep; annual duration is not specified.
Water is available to plants throughout most of the growing season in humid
regions. Wetness does not inhibit
growth of roots for significant periods during
most growing seasons. The soils are mainly free of features that are related to
wetness.
Moderately Well Drained
Water is removed from the soil somewhat slowly during some periods of the
year. Internal free water occurrence commonly is moderately deep and transitory
through permanent. The soils are wet for only a short time within the rooting
depth during the growing season, but long enough that most mesophytic crops
are affected. They commonly have a moderately low or lower saturated
hydraulic conductivity in a layer
within the upper 1 m, periodically receive high
rainfall, or both.
Somewhat Poorly Drained
Water is removed slowly so
that the soil is wet at a shallow depth for significant
periods during the growing season. The occurrence of internal free water
commonly is shallow to moderately deep and transitory to permanent. Wetness
markedly restricts the growth of
mesophytic crops, unless artificial drainage is
provided. The soils commonly have one or more of the following
characteristics: low or very low saturated hydraulic conductivity, a high water
table, additional water from seepage, or nearly continuous rainfall.
Poorly Drained
Water is removed so slowly that the soil is wet at shallow depths periodically
during the growing season or remains wet for long periods. The occurrence of
internal free water is shallow or very shallow and common or persistent. Free
water is commonly at or near the surface long enough during the growing
season so that most mesophytic crops cannot be grown, unless the soil is
artificially drained. The soil, however, is not continuously wet directly below
plow-depth. Free water at shallow depth is usually present. This water table is
commonly the result of low or very low saturated hydraulic conductivity of
nearly continuous rainfall, or of a combination of these.
Very Poorly Drained
Water is removed from the soil so
slowly that free water remains at or very near
the ground surface during much of the growing season. The occurrence of
internal free water is very shallow and
persistent or permanent. Unless the soil is
Document last revised April 2010
3 Connecticut Environmental Conditions Online – www.cteco.uconn.edu
artificially drained, most mesophytic crops cannot be grown. The soils are
commonly level or depressed and frequently ponded.
If rainfall is high or nearly
continuous, slope gradients may be greater.
Not Rated
Soils have characteristics that show
extreme variability from one location to
another. Often these areas are urban land complexes or miscellaneous areas. An
on-site investigation is required to determine
soil conditions present at the site. """

==========================================================
class Plant(Organism):
    __tablename__ = 'plants'
    __mapper_args__ = {'polymorphic_identity': 'plant'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    plant_cycle: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    growth_habit: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    primary_use: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    secondary_uses: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)), nullable=True, default=None)
    max_height_m: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    min_temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    max_temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    water_requirement: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)


class Animal(Organism):
    __tablename__ = 'animals'
    __mapper_args__ = {'polymorphic_identity': 'animal'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    animal_class: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None,
        comment='mammalia, aves, insecta, arachnida...'
    )
    avg_weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    is_domestic: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)


class Fungus(Organism):
    __tablename__ = 'fungi'
    __mapper_args__ = {'polymorphic_identity': 'fungus'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    fungus_use: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None,
        comment='inoculant, food, biocontrol...'
    )


class Bacterium(Organism):
    __tablename__ = 'bacteria'
    __mapper_args__ = {'polymorphic_identity': 'bacterium'}

    organism_id: Mapped[UUID] = mapped_column(
        ForeignKey('organisms.id'), primary_key=True, init=False
    )
    strain: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    bacterium_use: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None,
        comment='inoculant, biocontrol, biofertilizer...'
    )


=================================
========== SEEDS ==================
# seeds/production/required_data.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.domain.accounts.models.rbac import Role, Permission, RolePermission, UserRole
from app.domain.accounts.models.account import Account
from app.domain.accounts.models.user import User
from app.domain.accounts.enums import AccountPlan
from app.domain.organisms.models.organism_trait import OrganismTrait
from app.shared.enums import Resource, Action, TraitCategory
from app.shared.security import hash_password
from config.settings import settings


# ========== PERMISSIONS MATRIX ==========
PERMISSIONS_MATRIX = {
    'superuser': [
        (Resource.ACCOUNT, Action.CREATE),
        (Resource.ACCOUNT, Action.UPDATE),
        (Resource.ACCOUNT, Action.ARCHIVE),
        (Resource.USER, Action.CREATE),
        (Resource.USER, Action.UPDATE),
        (Resource.USER, Action.DEACTIVATE),
        (Resource.ESTATE, Action.APPROVE),
    ],
    'admin': [
        (Resource.ACCOUNT, Action.UPDATE),
        (Resource.USER, Action.CREATE),
        (Resource.USER, Action.UPDATE),
        (Resource.USER, Action.DEACTIVATE),
        (Resource.ESTATE, Action.CREATE),
        (Resource.ESTATE, Action.UPDATE),
        (Resource.ESTATE, Action.ARCHIVE),
        (Resource.ESTATE, Action.EXPORT),
        (Resource.FIELD, Action.CREATE),
        (Resource.FIELD, Action.UPDATE),
        (Resource.FIELD, Action.ARCHIVE),
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.CANCEL),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.CREATE),
        (Resource.TASK, Action.UPDATE),
        (Resource.TASK, Action.ASSIGN),
        (Resource.TASK, Action.CANCEL),
        (Resource.TASK, Action.EXPORT),
    ],
    'manager': [
        (Resource.ESTATE, Action.UPDATE),
        (Resource.ESTATE, Action.EXPORT),
        (Resource.FIELD, Action.CREATE),
        (Resource.FIELD, Action.UPDATE),
        (Resource.FIELD, Action.ARCHIVE),
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.CANCEL),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.CREATE),
        (Resource.TASK, Action.UPDATE),
        (Resource.TASK, Action.ASSIGN),
        (Resource.TASK, Action.CANCEL),
        (Resource.TASK, Action.EXPORT),
    ],
    'agronomist': [
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.ESTATE, Action.EXPORT),
    ],
    'worker': [
        (Resource.ACTIVITY, Action.EXECUTE),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.EXECUTE),
        (Resource.TASK, Action.EXPORT),
    ],
}


# ========== ORGANISM TRAITS ==========
INITIAL_TRAITS = [
    # Breeding methods
    {'name': 'conventional_hybrid', 'category': TraitCategory.BREEDING_METHOD, 'description': 'F1 hybrid from conventional breeding'},
    {'name': 'conventional_open_pollinated', 'category': TraitCategory.BREEDING_METHOD, 'description': 'Open-pollinated, seeds can be saved'},
    {'name': 'clonal', 'category': TraitCategory.BREEDING_METHOD, 'description': 'Vegetatively propagated (cuttings, grafts)'},
    {'name': 'gene_edited', 'category': TraitCategory.BREEDING_METHOD, 'description': 'CRISPR/TALEN edited — not classified as GMO in Brazil (CTNBio)'},
    {'name': 'synthetic', 'category': TraitCategory.BREEDING_METHOD, 'description': 'Synthetic variety from multiple inbred lines'},

    # Genetic modification
    {'name': 'gmo', 'category': TraitCategory.GENETIC_MODIFICATION, 'description': 'Single-stack GMO'},
    {'name': 'gmo_stacked', 'category': TraitCategory.GENETIC_MODIFICATION, 'description': 'Multiple GMO stacks (RR+BT)'},
    {'name': 'non_gmo', 'category': TraitCategory.GENETIC_MODIFICATION, 'description': 'Verified non-GMO'},

    # Origin
    {'name': 'creole', 'category': TraitCategory.ORIGIN, 'description': 'Traditional variety adapted locally — regional/cultural connotation'},
    {'name': 'landrace', 'category': TraitCategory.ORIGIN, 'description': 'Traditional variety developed over generations in specific region'},
    {'name': 'heirloom', 'category': TraitCategory.ORIGIN, 'description': 'Open-pollinated variety >50 years'},

    # Certification
    {'name': 'organic_certified', 'category': TraitCategory.CERTIFICATION, 'description': 'Certified organic'},
    {'name': 'biodynamic', 'category': TraitCategory.CERTIFICATION, 'description': 'Demeter certified — biodynamic production philosophy'},
    {'name': 'rainforest_alliance', 'category': TraitCategory.CERTIFICATION, 'description': 'Rainforest Alliance certified'},
    {'name': 'fair_trade', 'category': TraitCategory.CERTIFICATION, 'description': 'Fair trade certified'},
    {'name': 'globalgap', 'category': TraitCategory.CERTIFICATION, 'description': 'Good Agricultural Practices certified'},

    # Quality
    {'name': 'high_oleic', 'category': TraitCategory.QUALITY, 'description': 'High oleic acid content'},
    {'name': 'high_protein', 'category': TraitCategory.QUALITY, 'description': 'High protein content'},
    {'name': 'high_yield', 'category': TraitCategory.QUALITY, 'description': 'Bred for high productivity'},
    {'name': 'drought_adapted', 'category': TraitCategory.QUALITY, 'description': 'Adapted for low water availability'},

    # Resistance
    {'name': 'herbicide_tolerant', 'category': TraitCategory.RESISTANCE, 'description': 'Tolerant to specific herbicides — RR, Liberty Link'},
    {'name': 'insect_resistant', 'category': TraitCategory.RESISTANCE, 'description': 'Bt insect resistance'},
    {'name': 'disease_resistant', 'category': TraitCategory.RESISTANCE, 'description': 'Resistant to specific diseases'},
    {'name': 'nematode_resistant', 'category': TraitCategory.RESISTANCE, 'description': 'Resistant to nematodes'},

    # Breed
    {'name': 'purebred', 'category': TraitCategory.BREED, 'description': 'Registered purebred animal'},
    {'name': 'crossbred', 'category': TraitCategory.BREED, 'description': 'Cross between two or more breeds'},

    # Adaptation
    {'name': 'tropically_adapted', 'category': TraitCategory.ADAPTATION, 'description': 'Adapted to tropical climate — zebu base'},
    {'name': 'temperate_adapted', 'category': TraitCategory.ADAPTATION, 'description': 'Adapted to temperate climate — taurine base'},
]


# ========== SEED FUNCTIONS ==========
async def seed_permissions(session: AsyncSession) -> dict[tuple, Permission]:
    all_pairs = {
        (resource, action)
        for permissions in PERMISSIONS_MATRIX.values()
        for resource, action in permissions
    }
    for resource, action in all_pairs:
        await session.execute(
            insert(Permission)
            .values(resource=resource.value, action=action.value)
            .on_conflict_do_nothing(constraint='uq_permissions_resource_action')
        )
    await session.flush()

    result = await session.scalars(select(Permission))
    return {
        (p.resource, p.action): p
        for p in result.all()
    }


async def seed_roles(
    session: AsyncSession,
    permission_map: dict[tuple, Permission],
) -> None:
    for role_name, permissions in PERMISSIONS_MATRIX.items():
        await session.execute(
            insert(Role)
            .values(name=role_name)
            .on_conflict_do_nothing(constraint='uq_roles_name')
        )
        await session.flush()

        role = await session.scalar(
            select(Role).where(Role.name == role_name)
        )
        for resource, action in permissions:
            permission = permission_map[(resource.value, action.value)]
            await session.execute(
                insert(RolePermission)
                .values(role_id=role.id, permission_id=permission.id)
                .on_conflict_do_nothing()
            )

    await session.flush()


async def seed_superuser(session: AsyncSession) -> None:
    existing = await session.scalar(
        select(User).where(User.email == settings.SUPERADMIN_EMAIL)
    )
    if existing:
        return

    account = Account(
        name='Institutional',
        document='00000000000000',
        plan=AccountPlan.ENTERPRISE,
    )
    session.add(account)
    await session.flush()

    user = User(
        name='Super Admin',
        email=settings.SUPERADMIN_EMAIL,
        password=hash_password(settings.SUPERADMIN_PASSWORD),
        account_id=account.id,
    )
    session.add(user)
    await session.flush()

    superuser_role = await session.scalar(
        select(Role).where(Role.name == 'superuser')
    )
    await session.execute(
        insert(UserRole)
        .values(user_id=user.id, role_id=superuser_role.id)
        .on_conflict_do_nothing()
    )
    await session.flush()


async def seed_organism_traits(session: AsyncSession) -> None:
    for trait in INITIAL_TRAITS:
        await session.execute(
            insert(OrganismTrait)
            .values(
                name=trait['name'],
                category=trait['category'].value,
                description=trait['description'],
            )
            .on_conflict_do_nothing(constraint='uq_organism_trait_name')
        )
    await session.flush()


async def run(session: AsyncSession) -> None:
    print('Seeding permissions...')
    permission_map = await seed_permissions(session)

    print('Seeding roles...')
    await seed_roles(session, permission_map)

    print('Seeding superuser...')
    await seed_superuser(session)

    print('Seeding organism traits...')
    await seed_organism_traits(session)

    await session.commit()
    print('✓ Seed completed successfully.')


if __name__ == '__main__':
    async def main():
        engine = create_async_engine(settings.DATABASE_URL)
        async with AsyncSession(engine, expire_on_commit=False) as session:
            await run(session)

    asyncio.run(main())
