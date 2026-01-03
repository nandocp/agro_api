from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agro_api.entities.user import User
from tests.factories.users import UserFactory


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time, mock_id):
    time_columns = [
        'created_at',
        'updated_at',
        'last_sign_in_at',
        'current_sign_in_at',
    ]

    with mock_db_time(model=User, columns=time_columns) as time:
        with mock_id(model=User) as id:
            new_user = UserFactory.stub()
            user_data = User(
                name=new_user.name,
                email=new_user.email,
                password=new_user.password,
            )

            session.add(user_data)
            await session.commit()

            user = await session.scalar(
                select(User).where(User.email == new_user.email)
            )

    assert asdict(user) == {
        'id': id,
        'name': new_user.name,
        'email': new_user.email,
        'password': new_user.password,
        'created_at': time,
        'updated_at': time,
        'last_sign_in_at': time,
        'current_sign_in_at': time,
        'deleted_at': None,
        'is_active': True,
        'jti': None,
        'estates': [],
    }
