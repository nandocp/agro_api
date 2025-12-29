from dataclasses import asdict

from sqlalchemy import select

from agro_api.entities.user import User


def test_create_user(db_session, mock_db_time, mock_id):
    time_columns = [
        'created_at',
        'updated_at',
        'last_sign_in_at',
        'current_sign_in_at',
    ]

    with mock_db_time(model=User, columns=time_columns) as time:
        with mock_id(model=User) as id:
            new_user = User(
                username='euzinho', email='euzinho@teste.br', password='123456'
            )

            db_session.add(new_user)
            db_session.commit()

            user = db_session.scalar(
                select(User).where(User.email == 'euzinho@teste.br')
            )

    assert asdict(user) == {
        'id': id,
        'username': 'euzinho',
        'email': 'euzinho@teste.br',
        'password': '123456',
        'created_at': time,
        'updated_at': time,
        'last_sign_in_at': time,
        'current_sign_in_at': time,
    }
