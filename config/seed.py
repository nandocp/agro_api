from agro_api.entities.plant import PlantTrait
from agro_api.entities.plant import TraitCategory


# This is data, not code - but it's your controlled set
initial_traits = [
    # Breeding methods
    PlantTrait(name='conventional_hybrid', category=TraitCategory.BREEDING_METHOD,
          description='F1 hybrid from conventional breeding'),
    PlantTrait(name='conventional_open_pollinated', category=TraitCategory.BREEDING_METHOD,
          description='Open-pollinated, seeds can be saved'),
    PlantTrait(name='clonal', category=TraitCategory.BREEDING_METHOD,
          description='Vegetatively propagated (cuttings, grafts)'),
    PlantTrait(name='gene_edited', category=TraitCategory.BREEDING_METHOD,
          description='CRISPR/TALEN edited'),

    # Genetic modification
    PlantTrait(name='gmo', category=TraitCategory.GENETIC_MODIFICATION,
          description='Single-trait GMO'),
    PlantTrait(name='gmo_stacked', category=TraitCategory.GENETIC_MODIFICATION,
          description='Multiple GMO traits (RR+BT)'),

    # Origin
    PlantTrait(name='creole', category=TraitCategory.ORIGIN,
          description='Traditional landrace adapted locally'),
    PlantTrait(name='heirloom', category=TraitCategory.ORIGIN,
          description='Open-pollinated variety >50 years'),

    # Certification
    PlantTrait(name='organic_certified', category=TraitCategory.CERTIFICATION,
          description='Certified organic'),
    PlantTrait(name='biodynamic', category=TraitCategory.CERTIFICATION,
          description='Demeter certified'),

    # Quality (examples)
    PlantTrait(name='high_oleic', category=TraitCategory.QUALITY,
          description='High oleic acid content'),
    PlantTrait(name='high_protein', category=TraitCategory.QUALITY,
          description='High protein content'),
]
