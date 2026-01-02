from datetime import datetime
from random import choice

import factory

from agro_api.entities.estate import Estate, EstateKind

Faker = factory.Faker


class EstateFactory(factory.Factory):
    class Meta:
        model = Estate

    label = Faker('word')
    slug = Faker('word')
    opened_at = datetime.now()
    kind = choice(list(EstateKind)).value


class ClosedEstateFactory(EstateFactory):
    closed_at = datetime.now()
