from http import HTTPStatus
from secrets import token_hex

import pytest

from app.shared.security import hash_password
from tests.factories.accounts import UserFactory


@pytest.mark.asyncio
async def test_login_existing_user(client, account, session):
    password = token_hex(6)
    user = await UserFactory.create(
        session, password=hash_password(password), account_id=account.id
    )

    login_data = {
        'username': user.email,
        'password': password,
        'account_id': str(user.account_id),
    }

    response = await client.post('/auth/login', json=login_data)

    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['access_token'] is not None
    assert body['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_login_with_wrong_password(client, account, session):
    user = await UserFactory.create(session, account_id=account.id)

    login_data = {
        'username': user.email,
        'password': token_hex(6),
        'account_id': str(account.id),
    }

    response = await client.post('/auth/login', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    body = response.json()
    assert body['code'] == 'auth.invalid_credentials'
    assert not body['message']


@pytest.mark.asyncio
async def test_login_non_existing_user(client, account):
    user = await UserFactory.build()

    login_data = {
        'username': user.email,
        'password': token_hex(6),
        'account_id': str(account.id),
    }

    response = await client.post('/auth/login', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    body = response.json()
    assert body['code'] == 'auth.invalid_credentials'
    assert not body['message']
