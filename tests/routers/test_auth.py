from http import HTTPStatus
from secrets import token_hex

# import pytest
from config.password import hash_password
from tests.factories.users import UserFactory


# @pytest.mark.skip
def test_login_with_nonexistent_user(client):
    response = client.post(
        '/auth/login', data={'username': 'euzinho@eu.br', 'password': '123456'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.skip
def test_login_with_wrong_password(client, session):
    user = UserFactory.create()
    session.add(user)
    session.commit()

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': '123456'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.skip
def test_login_with_correct_credentials(client, session):
    pwd = token_hex(4)
    user = UserFactory.create()
    user.password = hash_password(pwd)
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': pwd}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert 'Authorization' in response.headers
    assert response.headers['Authorization-Type'] == 'Bearer'
    # assert user.current_sign_in_at == time
    # assert user.last_sign_in_at == time


# @pytest.mark.skip
def test_login_after_register(client):
    pwd = token_hex(4)
    user = UserFactory.build()

    client.post(
        '/users',
        json={
            'name': user.name,
            'email': user.email,
            'password': pwd
        }
    )

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': pwd}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert 'Authorization' in response.headers
    assert response.headers['Authorization-Type'] == 'Bearer'
