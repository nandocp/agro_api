from random import randint
from secrets import token_hex

import factory

from app.domain.accounts.models import Account, User
from app.shared.security import hash_password

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
        exclude = 'pwd'

    pwd = token_hex(4)
    name = Faker('name_nonbinary')
    email = Faker('ascii_free_email')
    password = hash_password(pwd)
    account_id = None
