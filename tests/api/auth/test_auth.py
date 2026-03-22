from datetime import datetime, timedelta
from http import HTTPStatus
from secrets import token_hex
from uuid import uuid7

import pytest

from app.domain.accounts.auth import encode_payload
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
async def test_login_locking_user(client, account, session):
    user = await UserFactory.create(session, account_id=account.id)
    user.failed_attempts = 4

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


@pytest.mark.asyncio
async def test_login_locked_user(client, account, session):
    user = await UserFactory.create(session, account_id=account.id)
    user.locked_at = datetime.now() - timedelta(minutes=1)
    session.add(user)
    await session.commit()

    login_data = {
        'username': user.email,
        'password': token_hex(6),
        'account_id': str(account.id),
    }

    response = await client.post('/auth/login', json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_logout(client, token):
    logout_response = await client.delete(
        '/auth/logout', headers={'Authorization': f'Bearer {token}'}
    )

    assert logout_response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_refresh_token(client, token):
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['access_token'] is not None
    assert body['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_refresh_token_missing_sub(client):
    token = encode_payload({'data': 'test', 'jti': 'jti'})
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_missing_jti(client):
    token = encode_payload({'data': 'test', 'sub': 'sub'})
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_expired(client):
    past = datetime.now() - timedelta(minutes=1)
    token = encode_payload({'jti': 'jti', 'sub': 'sub', 'exp': past})
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['code'] == 'auth.token_expired'


@pytest.mark.asyncio
async def test_refresh_token_no_user(client):
    token = encode_payload({'jti': str(uuid7()), 'sub': str(uuid7())})
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_mismatching_user_sub(client, user, session):
    jti = uuid7()
    user.jti = jti
    session.add(user)
    await session.commit()

    token = encode_payload({'jti': str(uuid7()), 'sub': str(user.id)})
    response = await client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
