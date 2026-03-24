from http import HTTPStatus

import pytest

from config.settings import settings
from tests.factories.accounts import UserFactory

SYSTEM_PATH = '/system/users'


@pytest.mark.asyncio
async def test_list_users(client, superuser_token, session, account):
    await UserFactory.create_batch(20, session=session, account_id=account.id)

    response = await client.get(
        SYSTEM_PATH,
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['data']) == settings.PAGINATION_LIMIT
