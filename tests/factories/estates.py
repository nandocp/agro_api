from datetime import datetime
from secrets import token_hex
from uuid import uuid4

# from random import choice
import factory
import factory.fuzzy

from agro_api.entities.estate import Estate, EstateKind

Faker = factory.Faker


class EstateFactory(factory.Factory):
    class Meta:
        model = Estate

    label = Faker('word')
    slug = factory.LazyFunction(token_hex)
    opened_at = datetime.now()
    kind = factory.fuzzy.FuzzyChoice(EstateKind)
    user_id = uuid4


class ClosedEstateFactory(EstateFactory):
    closed_at = datetime.now()
