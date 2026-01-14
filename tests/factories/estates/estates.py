from datetime import datetime

# from random import choice
import factory
import factory.fuzzy

from agro_api.entities.estate import Estate, EstateKind
from tests.factories.core import AccountFactory

Faker = factory.Faker


class EstateFactory(factory.Factory):
    class Meta:
        model = Estate

    label = Faker('word')
    slug = factory.Sequence(lambda n: f'est#{n}')
    description = Faker('sentence')
    opened_at = datetime.now()
    kind = factory.fuzzy.FuzzyChoice(EstateKind)
    account = factory.SubFactory(AccountFactory)
    account_id = factory.LazyAttribute(lambda obj: str(obj.account.id))
