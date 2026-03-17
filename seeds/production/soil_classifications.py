# seeds/production/soil_classifications.py

SOIL_CLASSIFICATIONS = [
    # ========== SiBCS ==========
    # Ordens (nível 1)
    {
        'name': 'Argissolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B textural com argila de atividade baixa',
    },
    {
        'name': 'Cambissolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B incipiente',
    },
    {
        'name': 'Chernossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte A chernozêmico e argila de atividade alta',
    },
    {
        'name': 'Espodossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B espódico',
    },
    {
        'name': 'Gleissolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos hidromórficos com horizonte glei',
    },
    {
        'name': 'Latossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B latossólico, altamente intemperizados',
    },
    {
        'name': 'Luvissolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B textural com argila de atividade alta',
    },
    {
        'name': 'Neossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com pequena expressão dos processos pedogenéticos',
    },
    {
        'name': 'Nitossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com horizonte B nítico',
    },
    {
        'name': 'Organossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com material orgânico',
    },
    {
        'name': 'Planossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com mudança textural abrupta e horizonte adensado',
    },
    {
        'name': 'Plintossolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com plintita ou petroplintita',
    },
    {
        'name': 'Vertissolos',
        'source': 'SiBCS',
        'parent': None,
        'description': 'Solos com alto teor de argila expansiva',
    },
    # Subgrupos de Latossolos (nível 2)
    {
        'name': 'Latossolos Vermelhos',
        'source': 'SiBCS',
        'parent': 'Latossolos',
        'description': 'Latossolos com matiz 2,5YR ou mais vermelho',
    },
    {
        'name': 'Latossolos Vermelho-Amarelos',
        'source': 'SiBCS',
        'parent': 'Latossolos',
        'description': 'Latossolos com matiz 5YR',
    },
    {
        'name': 'Latossolos Amarelos',
        'source': 'SiBCS',
        'parent': 'Latossolos',
        'description': 'Latossolos com matiz 6YR ou mais amarelo',
    },
    {
        'name': 'Latossolos Bruno',
        'source': 'SiBCS',
        'parent': 'Latossolos',
        'description': 'Latossolos de clima subtropical',
    },
    {
        'name': 'Latossolos Húmicos',
        'source': 'SiBCS',
        'parent': 'Latossolos',
        'description': 'Latossolos com horizonte A húmico',
    },
    # Subgrupos de Argissolos (nível 2)
    {
        'name': 'Argissolos Vermelhos',
        'source': 'SiBCS',
        'parent': 'Argissolos',
        'description': 'Argissolos com matiz 2,5YR ou mais vermelho',
    },
    {
        'name': 'Argissolos Vermelho-Amarelos',
        'source': 'SiBCS',
        'parent': 'Argissolos',
        'description': 'Argissolos com matiz 5YR',
    },
    {
        'name': 'Argissolos Amarelos',
        'source': 'SiBCS',
        'parent': 'Argissolos',
        'description': 'Argissolos com matiz 6YR ou mais amarelo',
    },
    {
        'name': 'Argissolos Acinzentados',
        'source': 'SiBCS',
        'parent': 'Argissolos',
        'description': 'Argissolos com cores acinzentadas',
    },
    # Subgrupos de Neossolos (nível 2)
    {
        'name': 'Neossolos Litólicos',
        'source': 'SiBCS',
        'parent': 'Neossolos',
        'description': 'Solos rasos com contato lítico',
    },
    {
        'name': 'Neossolos Flúvicos',
        'source': 'SiBCS',
        'parent': 'Neossolos',
        'description': 'Solos de origem fluvial',
    },
    {
        'name': 'Neossolos Quartzarênicos',
        'source': 'SiBCS',
        'parent': 'Neossolos',
        'description': 'Solos arenosos profundos',
    },
    {
        'name': 'Neossolos Regolíticos',
        'source': 'SiBCS',
        'parent': 'Neossolos',
        'description': 'Solos com contato lítico fragmentário',
    },
    # Subgrupos de Cambissolos (nível 2)
    {
        'name': 'Cambissolos Húmicos',
        'source': 'SiBCS',
        'parent': 'Cambissolos',
        'description': 'Cambissolos com horizonte A húmico',
    },
    {
        'name': 'Cambissolos Hápicos',
        'source': 'SiBCS',
        'parent': 'Cambissolos',
        'description': 'Cambissolos sem características diferenciais',
    },
    {
        'name': 'Cambissolos Flúvicos',
        'source': 'SiBCS',
        'parent': 'Cambissolos',
        'description': 'Cambissolos de origem fluvial',
    },
    # ========== WRB ==========
    # Reference Soil Groups (nível 1)
    {
        'name': 'Acrisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with low activity clay accumulation — strongly weathered',
    },
    {
        'name': 'Alisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with high activity clay accumulation and low base saturation',
    },
    {
        'name': 'Andosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils from volcanic material',
    },
    {
        'name': 'Arenosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Sandy soils',
    },
    {
        'name': 'Cambisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with incipient subsurface weathering',
    },
    {
        'name': 'Chernozems',
        'source': 'WRB',
        'parent': None,
        'description': 'Black soils with high organic matter and base saturation',
    },
    {
        'name': 'Ferralsols',
        'source': 'WRB',
        'parent': None,
        'description': 'Highly weathered tropical soils — equivalent to Latossolos',
    },
    {
        'name': 'Fluvisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Floodplain soils',
    },
    {
        'name': 'Gleysols',
        'source': 'WRB',
        'parent': None,
        'description': 'Waterlogged soils with gley horizon',
    },
    {
        'name': 'Histosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Organic soils',
    },
    {
        'name': 'Kastanozems',
        'source': 'WRB',
        'parent': None,
        'description': 'Chestnut colored soils of dry steppes',
    },
    {
        'name': 'Leptosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Shallow soils over hard rock',
    },
    {
        'name': 'Lixisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with low activity clay accumulation and high base saturation',
    },
    {
        'name': 'Luvisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with high activity clay accumulation and high base saturation',
    },
    {
        'name': 'Nitisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Deep red tropical soils with nitic horizon',
    },
    {
        'name': 'Phaeozems',
        'source': 'WRB',
        'parent': None,
        'description': 'Dark soils with high base saturation',
    },
    {
        'name': 'Planosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with abrupt textural change and stagnic conditions',
    },
    {
        'name': 'Plinthosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with plinthite or petroplinthite',
    },
    {
        'name': 'Podzols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with spodic horizon',
    },
    {
        'name': 'Regosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Weakly developed soils in unconsolidated material',
    },
    {
        'name': 'Solonchaks',
        'source': 'WRB',
        'parent': None,
        'description': 'Salt-affected soils',
    },
    {
        'name': 'Solonetz',
        'source': 'WRB',
        'parent': None,
        'description': 'Sodium-rich soils',
    },
    {
        'name': 'Stagnosols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with stagnic conditions',
    },
    {
        'name': 'Umbrisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Soils with dark organic-rich horizon and low base saturation',
    },
    {
        'name': 'Vertisols',
        'source': 'WRB',
        'parent': None,
        'description': 'Shrink-swell clay soils',
    },
    # WRB Qualifiers for Ferralsols (nível 2)
    {
        'name': 'Haplic Ferralsols',
        'source': 'WRB',
        'parent': 'Ferralsols',
        'description': 'Ferralsols without other diagnostic features',
    },
    {
        'name': 'Xanthic Ferralsols',
        'source': 'WRB',
        'parent': 'Ferralsols',
        'description': 'Yellow Ferralsols',
    },
    {
        'name': 'Rhodic Ferralsols',
        'source': 'WRB',
        'parent': 'Ferralsols',
        'description': 'Red Ferralsols',
    },
    {
        'name': 'Humic Ferralsols',
        'source': 'WRB',
        'parent': 'Ferralsols',
        'description': 'Ferralsols with humic horizon',
    },
    # WRB Qualifiers for Acrisols (nível 2)
    {
        'name': 'Haplic Acrisols',
        'source': 'WRB',
        'parent': 'Acrisols',
        'description': 'Acrisols without other diagnostic features',
    },
    {
        'name': 'Humic Acrisols',
        'source': 'WRB',
        'parent': 'Acrisols',
        'description': 'Acrisols with humic horizon',
    },
    {
        'name': 'Ferric Acrisols',
        'source': 'WRB',
        'parent': 'Acrisols',
        'description': 'Acrisols with ferric horizon',
    },
]


async def seed_soil_classifications(session: AsyncSession) -> None:
    """Seed soil classifications — idempotente."""

    # primeiro insere os pais (parent=None)
    for item in SOIL_CLASSIFICATIONS:
        if item['parent'] is not None:
            continue
        await session.execute(
            insert(SoilClassification)
            .values(
                name=item['name'],
                source=item['source'],
                description=item['description'],
                parent_id=None,
            )
            .on_conflict_do_nothing(
                constraint='uq_soil_classification_name_source'
            )
        )
    await session.flush()

    # depois insere os filhos resolvendo parent_id
    for item in SOIL_CLASSIFICATIONS:
        if item['parent'] is None:
            continue

        parent = await session.scalar(
            select(SoilClassification).where(
                SoilClassification.name == item['parent'],
                SoilClassification.source == item['source'],
            )
        )
        if not parent:
            print(f'✗ Parent not found: {item["parent"]} ({item["source"]})')
            continue

        await session.execute(
            insert(SoilClassification)
            .values(
                name=item['name'],
                source=item['source'],
                description=item['description'],
                parent_id=parent.id,
            )
            .on_conflict_do_nothing(
                constraint='uq_soil_classification_name_source'
            )
        )
    await session.flush()
    print('✓ Soil classifications seeded')
