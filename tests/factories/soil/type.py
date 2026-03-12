import factory

from agro_api.entities.soil import SoilType

Faker = factory.Faker


class SoilTypeFactory(factory.Factory):
    class Meta:
        model = SoilType

    name = Faker('word')
    source = Faker('word')
