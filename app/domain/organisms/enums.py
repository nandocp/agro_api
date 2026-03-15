from enum import Enum


class Kingdom(str, Enum):
    PLANTAE = 'plantae'
    ANIMALIA = 'animalia'
    FUNGI = 'fungi'
    BACTERIA = 'bacteria'
    CHROMISTA = 'chromista'


class TraitCategory(str, Enum):
    """High-level classification of trait categories."""

    BREEDING_METHOD = 'breeding_method'  # How it was developed
    GENETIC_MODIFICATION = 'genetic_modification'  # GMO status
    CERTIFICATION = 'certification'  # Organic, etc.
    ORIGIN = 'origin'  # Heirloom, creole, etc.
    QUALITY = 'quality'  # High oleic, etc.
    RESISTANCE = 'resistance'  # Pest/disease resistance


class PlantUse(str, Enum):
    GRAIN = 'grain'  # soy, corn, wheat
    FRUIT = 'fruit'  # orange, mango, coffee (cherry)
    TIMBER = 'timber'  # eucalyptus, mogno, pine
    FIBER = 'fiber'  # cotton, jute
    FORAGE = 'forage'  # pasture grasses, alfalfa
    OIL = 'oil'  # palm, sunflower
    NUT = 'nut'  # cashew, walnut
    ORNAMENTAL = 'ornamental'  # flowers, landscaping
    MEDICINAL = 'medicinal'  # herbs
    SHADE = 'shade'  # nurse trees
    COVER_CROP = 'cover_crop'  # soil improvement
    GREEN_MANURE = 'green_manure'  # plowed-under crops


class WaterRequirement(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class PlantCycle(str, Enum):
    ANNUAL = 'annual'
    BIENNIAL = 'biennial'
    PERENNIAL = 'perennial'


class GrowthHabit(str, Enum):
    TREE = 'tree'
    SHRUB = 'shrub'
    BRUSH = 'brush'
    HERB = 'herb'
    CROP = 'crop'
    GRASS = 'grass'
    VINE = 'vine'
