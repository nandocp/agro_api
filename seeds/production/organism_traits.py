INITIAL_TRAITS = [
    # Breeding methods
    {
        'name': 'conventional_hybrid',
        'category': TraitCategory.BREEDING_METHOD,
        'description': 'F1 hybrid from conventional breeding',
    },
    {
        'name': 'conventional_open_pollinated',
        'category': TraitCategory.BREEDING_METHOD,
        'description': 'Open-pollinated, seeds can be saved',
    },
    {
        'name': 'clonal',
        'category': TraitCategory.BREEDING_METHOD,
        'description': 'Vegetatively propagated (cuttings, grafts)',
    },
    {
        'name': 'gene_edited',
        'category': TraitCategory.BREEDING_METHOD,
        'description': 'CRISPR/TALEN edited — not classified as GMO in Brazil (CTNBio)',
    },
    {
        'name': 'synthetic',
        'category': TraitCategory.BREEDING_METHOD,
        'description': 'Synthetic variety from multiple inbred lines',
    },
    # Genetic modification
    {
        'name': 'gmo',
        'category': TraitCategory.GENETIC_MODIFICATION,
        'description': 'Single-stack GMO',
    },
    {
        'name': 'gmo_stacked',
        'category': TraitCategory.GENETIC_MODIFICATION,
        'description': 'Multiple GMO stacks (RR+BT)',
    },
    {
        'name': 'non_gmo',
        'category': TraitCategory.GENETIC_MODIFICATION,
        'description': 'Verified non-GMO',
    },
    # Origin
    {
        'name': 'creole',
        'category': TraitCategory.ORIGIN,
        'description': 'Traditional variety adapted locally — regional/cultural connotation',
    },
    {
        'name': 'landrace',
        'category': TraitCategory.ORIGIN,
        'description': 'Traditional variety developed over generations in specific region',
    },
    {
        'name': 'heirloom',
        'category': TraitCategory.ORIGIN,
        'description': 'Open-pollinated variety >50 years',
    },
    # Certification
    {
        'name': 'organic_certified',
        'category': TraitCategory.CERTIFICATION,
        'description': 'Certified organic',
    },
    {
        'name': 'biodynamic',
        'category': TraitCategory.CERTIFICATION,
        'description': 'Demeter certified — biodynamic production philosophy',
    },
    {
        'name': 'rainforest_alliance',
        'category': TraitCategory.CERTIFICATION,
        'description': 'Rainforest Alliance certified',
    },
    {
        'name': 'fair_trade',
        'category': TraitCategory.CERTIFICATION,
        'description': 'Fair trade certified',
    },
    {
        'name': 'globalgap',
        'category': TraitCategory.CERTIFICATION,
        'description': 'Good Agricultural Practices certified',
    },
    # Quality
    {
        'name': 'high_oleic',
        'category': TraitCategory.QUALITY,
        'description': 'High oleic acid content',
    },
    {
        'name': 'high_protein',
        'category': TraitCategory.QUALITY,
        'description': 'High protein content',
    },
    {
        'name': 'high_yield',
        'category': TraitCategory.QUALITY,
        'description': 'Bred for high productivity',
    },
    {
        'name': 'drought_adapted',
        'category': TraitCategory.QUALITY,
        'description': 'Adapted for low water availability',
    },
    # Resistance
    {
        'name': 'herbicide_tolerant',
        'category': TraitCategory.RESISTANCE,
        'description': 'Tolerant to specific herbicides — RR, Liberty Link',
    },
    {
        'name': 'insect_resistant',
        'category': TraitCategory.RESISTANCE,
        'description': 'Bt insect resistance',
    },
    {
        'name': 'disease_resistant',
        'category': TraitCategory.RESISTANCE,
        'description': 'Resistant to specific diseases',
    },
    {
        'name': 'nematode_resistant',
        'category': TraitCategory.RESISTANCE,
        'description': 'Resistant to nematodes',
    },
    # Breed
    {
        'name': 'purebred',
        'category': TraitCategory.BREED,
        'description': 'Registered purebred animal',
    },
    {
        'name': 'crossbred',
        'category': TraitCategory.BREED,
        'description': 'Cross between two or more breeds',
    },
    # Adaptation
    {
        'name': 'tropically_adapted',
        'category': TraitCategory.ADAPTATION,
        'description': 'Adapted to tropical climate — zebu base',
    },
    {
        'name': 'temperate_adapted',
        'category': TraitCategory.ADAPTATION,
        'description': 'Adapted to temperate climate — taurine base',
    },
]


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
