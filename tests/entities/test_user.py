from dataclasses import asdict

from sqlalchemy import select

from agro_api.entities.user import User
from tests.factories.users import UserFactory


def test_create_user(session, mock_db_time, mock_id):
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
            session.commit()

            user = session.scalar(
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
    }
