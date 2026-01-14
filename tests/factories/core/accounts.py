from secrets import token_hex

import factory

from agro_api.entities.core import Account

Faker = factory.Faker


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    name = Faker('company')
    document = factory.LazyFunction(token_hex)
