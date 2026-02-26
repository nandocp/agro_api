# from uuid import uuid4

import factory

from agro_api.entities.plot import Plot

# from tests.factories.core import UserFactory
# from tests.factories.estates import EstateFactory

Faker = factory.Faker


class PlotFactory(factory.Factory):
    class Meta:
        model = Plot

    # land_use = factory.fuzzy.FuzzyChoice(LandUses)
    # label = Faker('word')
    slug = factory.Sequence(lambda n: f'plot#{n}')
    # status = factory.fuzzy.FuzzyChoice(PlotStatus)
    # estate = factory.SubFactory(EstateFactory)
    # creator = factory.SubFactory(UserFactory)
    # estate_id = factory.LazyAttribute(lambda obj: str(obj.estate.id))
    # creator_id = factory.LazyAttribute(lambda obj: str(obj.creator.id))
