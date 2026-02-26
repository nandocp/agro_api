from datetime import datetime

# from random import choice
import factory
import factory.fuzzy

from agro_api.entities.estate import Estate, EstateKind
from tests.factories.core import AccountFactory

Faker = factory.Faker


class EstateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Estate

    label = Faker('word')
    slug = factory.Sequence(lambda n: f'estate#{n}')
    description = Faker('sentence')
    started_at = factory.LazyFunction(datetime.now)
    kind = factory.fuzzy.FuzzyChoice(list(EstateKind))
    account = factory.SubFactory(AccountFactory)
    account_id = factory.LazyAttribute(lambda obj: obj.account.id)
