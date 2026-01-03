from datetime import datetime, timedelta
from secrets import token_hex

import factory

from agro_api.entities.user import User
from config.password import hash_password

Faker = factory.Faker


class UserFactory(factory.Factory):
    class Meta:
        model = User
        exclude = 'pwd'

    pwd = token_hex(4)
    name = Faker('name_nonbinary')
    email = Faker('ascii_free_email')
    password = hash_password(pwd)


class InactiveUserFactory(UserFactory):
    is_active = False


class DeletedUserFactory(UserFactory):
    deleted_at = datetime.now() - timedelta(seconds=30)
