from http import HTTPStatus
from secrets import token_hex

from faker import Faker
from sqlalchemy import select

from agro_api.entities.user import User


def test_create(client, session, mock_id):
    user_data = {
        'name': Faker().name_nonbinary(),
        'email': Faker().ascii_free_email(),
        'password': token_hex(4),
    }

    user_db = session.scalar(
        select(User).where(User.email == user_data['email'])
    )

    assert not user_db

    response = client.post('/users', json=user_data)
    user_db = session.scalar(
        select(User).where(User.email == user_data['email'])
    )

    assert user_db
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': user_data['name'],
        'email': user_data['email'],
        'id': str(user_db.id),
        'created_at': str(user_db.created_at).replace(' ', 'T'),
    }
