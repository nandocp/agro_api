from enum import Enum


class GeneticSource(str, Enum):
    """Origin of planting material."""
    FARM_SAVED = 'farm_saved'          # Saved from previous harvest
    CERTIFIED = 'certified'            # Certified commercial seed
    LOCAL_EXCHANGE = 'local_exchange'  # Swapped with other farmers
    PURCHASED = 'purchased'            # Bought but not certified
    RESEARCH = 'research'              # From research institution
    UNKNOWN = 'unknown'


class PlantingArrangement(str, Enum):
    ROW = 'row'
    SCATTERED = 'scattered'
    CLUSTER = 'cluster'
    BROADCAST = 'broadcast'  # for seeds
    CONTOUR = 'contour'  # following terrain


class PlantingPurpose(str, Enum):
    # ========== PLANT PRODUCTION ==========
    # Annual crops (seasonal): corn, soy, wheat, rice, beans.
    CROPPING = 'cropping'

    # Forage crops (alfalfa, silage corn) important for livestock systems.
    FORAGE = 'forage'

    # Plants grown for fiber: cotton, flax, hemp, jute.
    FIBER = 'fiber'

    # Perennial crops (multi-year)
    # Fruit and nut trees: apples, oranges, walnuts, almonds.
    FRUIT_TREES = 'fruit_trees'

    # Trees grown for wood production (eucalyptus, pine).
    TIMBER_TREES = 'timber_trees'

    # Grapes, kiwis, other.
    VINE = 'vine'

    # Young plants for transplanting.
    NURSERY = 'nursery'

    # Flowers, landscaping plants, decorative crops.
    ORNAMENTAL = 'ornamental'

    # Vegetables, herbs
    HORTICULTURE = 'horticulture'


class PlantingStratum(str, Enum):
    CANOPY = 'canopy'  # E
    MIDSTORY = 'midstory'  # A
    UNDERSTORY = 'understory'  # M
    GROUND = 'ground'  # B


class ActivityType(str, Enum):
    """What people ARE DOING on the land (temporal, active).
    Activities transform inputs into outputs and can be chained
    across plots to form production systems.
    """

    # Note: Values are sorted by category:
    # Plant → Animal → Processing → Conservation → Other

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

    WOOL = 'wool'

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
