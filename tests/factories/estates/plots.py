import factory
import factory.fuzzy

from agro_api.entities.estate import Plot
from agro_api.entities.estate.plot import LandUses, PlotStatus

Faker = factory.Faker


class PlotFactory(factory.Factory):
    class Meta:
        model = Plot

    label = Faker('word')
    slug = factory.Sequence(lambda n: f'plot#{n}')
    land_use = factory.fuzzy.FuzzyChoice(LandUses)
    status = PlotStatus.active
