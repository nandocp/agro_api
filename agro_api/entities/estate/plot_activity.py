from agro_api.entities.base import BaseEntity

class ActivityType(str, Enum):
    """What people ARE DOING on the land (temporal, active).
    Activities transform inputs into outputs and can be chained
    across plots to form production systems.
    """

    # ========== PLANT PRODUCTION ==========
    # Annual crops (seasonal)
    CROPPING = 'cropping'
    """Annual crops: corn, soy, wheat, rice, beans.
       Inputs: seeds, fertilizer, water
       Outputs: grain, silage, straw"""

    FORAGE = 'forage'
    """
    Forage crops (alfalfa, silage corn) important for livestock systems.
    """

    FIBER = 'fiber'
    """Plants grown for fiber: cotton, flax, hemp, jute.
    Inputs: seeds, water, pest management
    Outputs: raw fiber for textiles, rope, paper"""

    # Perennial crops (multi-year)
    FRUIT_TREES = 'fruit_trees'
    """Perennial fruit/nut production (apples, oranges, walnuts).
        Fruit and nut trees: apples, oranges, walnuts, almonds.
        Inputs: saplings, pruning, pest control
        Outputs: fresh fruit, nuts, timber (at end of life)"""

    TIMBER_TREES = 'timber_trees'
    """Trees grown for wood production (eucalyptus, pine)."""

    VINE = 'vine'
    """Grapes, kiwis, other (wine, table).
       Inputs: cuttings, trellising, pest control
       Outputs: grapes, wine (if processed on-site)"""

    NURSERY = 'nursery'
    """Young plants for transplanting.
       Inputs: seeds, cuttings, growing media
       Outputs: seedlings, saplings for other plots"""

    ORNAMENTAL = 'ornamental'
    """Flowers, landscaping plants, decorative crops.
    Inputs: cuttings, seeds, greenhouse management
    Outputs: cut flowers, potted plants, landscaping material"""
    # ========== ANIMAL PRODUCTION ==========
    GRAZING = 'grazing'
    """Ruminants on pasture: cattle, sheep, goats.
       Inputs: pasture, water, supplements, veterinary
       Outputs: meat, milk, wool, manure"""

    FEEDLOT = 'feedlot'
    """Confined animal feeding.
       Inputs: feed (from storage), water, veterinary
       Outputs: meat, manure (concentrated)"""

    DAIRY = 'dairy'
    """Milk production.
       Inputs: feed, water, veterinary, milking equipment
       Outputs: milk, calves, cull cows, manure"""

    PIGS = 'pigs'
    """Swine production.
       Inputs: feed, water, veterinary, bedding
       Outputs: pork, piglets, manure"""

    POULTRY = 'poultry'
    """Chickens, turkeys, ducks.
       Inputs: feed, water, veterinary, housing
       Outputs: meat, eggs, litter"""

    AQUACULTURE = 'aquaculture'
    """Fish, shrimp, aquatic plants.
       Inputs: fingerlings, feed, water management
       Outputs: fish, shrimp, aquatic plants"""

    APICULTURE = 'apiculture'
    """Beekeeping.
       Inputs: hives, bees, management
       Outputs: honey, wax, pollination services"""

    # ========== PROCESSING & STORAGE ==========
    STORAGE = 'storage'
    """Silos, grain bins.
       Inputs: grain from CROPPING
       Outputs: stored grain, dried grain, feed for animals"""

    PROCESSING = 'processing'
    """General on-farm processing not covered by specific categories.
        Grinding, mixing feed.
        Inputs: grain, supplements, minerals
        Outputs: formulated feed for animals
        ---
        On-farm dairy processing.
        Inputs: raw milk
        Outputs: cheese, yogurt, pasteurized milk
        ---
        Production of alcoholic and non-alcoholic beverages.
        Includes cachaça, wine, beer, scotch, juices, ciders.
    """

    COMPOSTING = 'composting'
    """Converting organic waste to soil amendment.
       Inputs: manure, crop residue, food waste
       Outputs: compost, fertilizer"""

    BIOENERGY = 'bioenergy'
    """Biogas, biomass energy.
       Inputs: manure, crop residue
       Outputs: biogas, electricity, heat"""

    # ========== CONSERVATION & REST ==========
    FALLOW = 'fallow'
    """Land resting between production cycles.
       Inputs: none (or cover crop seeds)
       Outputs: soil recovery, nutrient accumulation"""

    CONSERVATION = 'conservation'
    """Active preservation management.
       Inputs: invasive species control, monitoring
       Outputs: biodiversity, ecosystem services"""

    REHABILITATION = 'rehabilitation'
    """Restoring degraded land.
       Inputs: soil amendments, native species planting
       Outputs: restored ecosystem, future productive land"""

    # ========== OTHER ==========
    RESEARCH = 'research'
    """Experimental plots, trials.
       Inputs: experimental treatments, monitoring
       Outputs: data, knowledge"""

    TOURISM = 'tourism'
    """Agritourism, farm stays.
       Inputs: facilities, staff
       Outputs: visitor experiences, education"""

    BIOLOGICAL_PRODUCTION = 'biological_production'
    """Cultivation of beneficial microorganisms for agricultural use.
       Includes:
       - Biocontrol agents (Trichoderma, Beauveria, Bacillus)
       - Biofertilizers (Rhizobium, Azospirillum, mycorrhizae)
       - Biopesticides (Bt, viruses, nematodes)
       - Compost teas and microbial inoculants

       This can occur in dedicated facilities (labs, fermenters) or
       in-field production (mulch layers, compost piles)."""


class PlotActivity(BaseEntity):
    __tablename__ = 'plot_activities'

    plot_id: Mapped[Uuid] = mapped_column(ForeignKey('plots.id'))
    activity_type: Mapped[ActivityType]  # 'cultivation', 'grazing', 'silvopasture'

    # Common fields
    started_at: Mapped[date]
    finished_at: Mapped[date | None]
    status: Mapped[ActivityStatus]
    creator_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))
    notes: Mapped[str | None]

    # Relationships to specializations (one-to-one)
    cultivation: Mapped['CultivationDetails'] = relationship(
        back_populates='activity',
        cascade='all, delete-orphan',
        uselist=False  # This makes it one-to-one
    )

    grazing: Mapped['GrazingDetails'] = relationship(
        back_populates='activity',
        cascade='all, delete-orphan',
        uselist=False
    )

    # Helper to get the right details object
    @property
    def details(self):
        if self.activity_type == ActivityType.CULTIVATION:
            return self.cultivation
        elif self.activity_type == ActivityType.GRAZING:
            return self.grazing
        return None


class CultivationDetails(Base):
    __tablename__ = 'cultivation_details'

    # Primary key is ALSO foreign key to PlotActivity
    activity_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plot_activities.id'),
        primary_key=True  # Shared primary key = one-to-one
    )

    # Cultivation-specific fields
    plant_species_id: Mapped[Uuid] = mapped_column(ForeignKey('plant_species.id'))
    planting_density: Mapped[int]
    row_spacing_cm: Mapped[int | None]

    # Relationship back
    activity: Mapped['PlotActivity'] = relationship(back_populates='cultivation')


class GrazingDetails(Base):
    __tablename__ = 'grazing_details'

    activity_id: Mapped[Uuid] = mapped_column(
        ForeignKey('plot_activities.id'),
        primary_key=True
    )

    # Grazing-specific fields
    animal_breed_id: Mapped[Uuid] = mapped_column(ForeignKey('animal_breeds.id'))
    head_count: Mapped[int]
    stocking_rate_ha: Mapped[float | None]

    activity: Mapped['PlotActivity'] = relationship(back_populates='grazing')
