from enum import Enum


class ActivityStatus(str, Enum):
    PLANNING = 'planning'
    EXECUTING = 'executing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class ActivityKind(str, Enum):
    """What people ARE DOING on the land (temporal, active).
    Activities transform inputs into outputs and can be chained
    across fields to form production systems.
    """

    # Note: Values are sorted by category:
    # Plant → Animal → Processing → Conservation → Other

    # ========== PLANTATION PRODUCTION ==========
    CROPPING = 'cropping'
    FORAGE = 'forage'
    FIBER = 'fiber'
    FRUIT_TREES = 'fruit_trees'
    TIMBER_TREES = 'timber_trees'
    VINE = 'vine'
    NURSERY = 'nursery'
    ORNAMENTAL = 'ornamental'

    # ========== ANIMAL PRODUCTION ==========
    # Ruminants on pasture: cattle, sheep, goats.
    GRAZING = 'grazing'

    # Confined animal feeding.
    FEEDLOT = 'feedlot'

    # Milk production.
    DAIRY = 'dairy'

    # Swine production.
    PIGS = 'pigs'

    # Chickens, turkeys, ducks.
    POULTRY = 'poultry'

    # Fish, shrimp, aquatic plants.
    AQUACULTURE = 'aquaculture'

    # Beekeeping.
    APICULTURE = 'apiculture'

    EQUINE = 'equine'

    # ========== PROCESSING & STORAGE ==========
    # Silos, grain bins.
    STORAGE = 'storage'

    # General on-farm processing not covered by specific categories.
    # MAY SPLIT LATER
    # FEED_PROCESSING, DAIRY_PROCESSING, BEVERAGE_PRODUCTION
    PROCESSING = 'processing'

    # Converting organic waste to soil amendment.
    COMPOSTING = 'composting'

    # Biogas, biomass energy.
    BIOENERGY = 'bioenergy'

    # ========== CONSERVATION & REST ==========
    # Land resting between production cycles.
    FALLOW = 'fallow'

    # Active preservation management.
    CONSERVATION = 'conservation'

    # Restoring degraded land.
    REHABILITATION = 'rehabilitation'

    # ========== OTHER ==========
    # Experimental plots, trials.
    RESEARCH = 'research'

    # Agritourism, farm stays.
    TOURISM = 'tourism'

    # Cultivation of beneficial microorganisms for agricultural use.
    BIOLOGICAL_PRODUCTION = 'biological_production'
