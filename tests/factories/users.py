from datetime import datetime, timedelta
from secrets import token_hex

import factory
from faker import Faker

from agro_api.entities.user import User

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    name = fake.name_nonbinary()
    email = fake.ascii_free_email()
    password = token_hex(4)


class InactiveUserFactory(UserFactory):
    is_active = False


class DeletedUserFactory(UserFactory):
    deleted_at = datetime.now() - timedelta(seconds=30)
