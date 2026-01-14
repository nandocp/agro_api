from datetime import datetime

# from random import choice
import factory
import factory.fuzzy

from agro_api.entities.estate import Estate, EstateKind
from tests.factories.users import UserFactory

Faker = factory.Faker


class EstateFactory(factory.Factory):
    class Meta:
        model = Estate

    label = Faker('word')
    slug = factory.Sequence(lambda n: f'est#{n}')
    opened_at = datetime.now()
    kind = factory.fuzzy.FuzzyChoice(EstateKind)
    description = Faker('sentence')
    user = factory.SubFactory(UserFactory)
