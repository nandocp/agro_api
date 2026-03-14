from http import HTTPStatus
from secrets import token_hex

import pytest

from tests.factories.accounts import UserFactory

BASE_PATH = '/api/auth'


@pytest.mark.asyncio
async def test_login_existing_user(client, account, session):
    password = token_hex(6)
    user = UserFactory.create(
        session, password=password, account_id=account.id
    )
    login_data = {'email': user.email, 'password': user.password}
    response = await client.post(f'{BASE_PATH}/login', json=login_data)

    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['access_token'] is not None
    assert body['token_type'] is not None
