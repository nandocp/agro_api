from random import randint

import factory

from app.domain.accounts.models import Account, User

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class AccountFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Account

    name = Faker('company')
    document = randint(11111111111111, 99999999999999)


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = User
