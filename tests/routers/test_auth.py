from http import HTTPStatus
from secrets import token_hex

import pytest

from config.password import hash_password
from tests.factories.users import UserFactory


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_login_with_nonexistent_user(client):
    response = client.post(
        '/auth/login', data={'username': 'euzinho@eu.br', 'password': '123456'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_login_with_incorrect_credentials(client, session):
    user = UserFactory.create()
    session.add(user)
    await session.commit()

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': '123456'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_login_with_correct_credentials(client, session):
    pwd = token_hex(4)
    user = UserFactory.create()
    user.password = hash_password(pwd)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': pwd}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert 'Authorization' in response.headers
    assert response.headers['Authorization-Type'] == 'Bearer'
    # assert user.current_sign_in_at == time
    # assert user.last_sign_in_at == time


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_login_after_register(client):
    pwd = token_hex(4)
    user = UserFactory.build()

    client.post(
        '/users',
        json={'name': user.name, 'email': user.email, 'password': pwd},
    )

    response = client.post(
        '/auth/login', data={'username': user.email, 'password': pwd}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert 'Authorization' in response.headers
    assert response.headers['Authorization-Type'] == 'Bearer'


def test_logout_logged_in_user(client, token, user):
    first_response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert first_response.status_code == HTTPStatus.OK

    logout_response = client.delete(
        '/auth/logout',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert logout_response.status_code == HTTPStatus.NO_CONTENT

    second_response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert second_response.status_code == HTTPStatus.UNAUTHORIZED
    assert not user.jti
