from enum import Enum


class GeneticSource(str, Enum):
    """Origin of planting material."""

    FARM_SAVED = 'farm_saved'  # Saved from previous harvest
    CERTIFIED = 'certified'  # Certified commercial seed
    LOCAL_EXCHANGE = 'local_exchange'  # Swapped with other farmers
    PURCHASED = 'purchased'  # Bought but not certified
    RESEARCH = 'research'  # From research institution
    UNKNOWN = 'unknown'


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
