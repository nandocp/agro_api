from random import choice
from secrets import token_hex

import factory
from br_cpf_cnpj import generate_random_cnpj, generate_random_cpf

from app.domain.accounts.models import Account, User
from app.shared.security import hash_password

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class AccountFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Account

    name = Faker('company')
    document = factory.LazyAttribute(
        lambda _: choice([
            generate_random_cpf(masked=True),
            generate_random_cnpj(alphanumeric=False, masked=True),
        ])
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
