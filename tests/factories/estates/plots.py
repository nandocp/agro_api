# from uuid import uuid4

import factory
import factory.fuzzy

from agro_api.entities.estate import Plot
from agro_api.entities.estate.plot import LandUses, PlotStatus
from tests.factories.estates import EstateFactory
from tests.factories.users import UserFactory

Faker = factory.Faker


class PlotFactory(factory.Factory):
    class Meta:
        model = Plot

    label = Faker('word')
    slug = factory.Sequence(lambda n: f'plot#{n}')
    land_use = factory.fuzzy.FuzzyChoice(LandUses)
    status = factory.fuzzy.FuzzyChoice(PlotStatus)
    estate = factory.SubFactory(EstateFactory)
    creator = factory.SubFactory(UserFactory)
