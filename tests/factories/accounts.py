from random import randint

import factory

from app.domain.accounts.models import Account, User

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class AccountFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Account

    name = Faker('company')
    document = factory.LazyAttribute(
        lambda _: randint(11111111111111, 99999999999999)
    )


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = User

    name = Faker('name_nonbinary')
    email = Faker('ascii_free_email')
