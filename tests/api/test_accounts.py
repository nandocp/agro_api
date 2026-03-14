from http import HTTPStatus

import pytest

from app.domain.accounts.models import Account
from app.shared.crud import CRUDBase
from tests.factories.accounts import AccountFactory

BASE_PATH = '/api/accounts'


@pytest.mark.asyncio
async def test_create_account_without_auth_headers(client):
    account = await AccountFactory.build()
    params = {'name': account.name, 'document': account.document}

    response = await client.post(BASE_PATH, json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_account_with_auth_headers(client, token, session):
    account = await AccountFactory.build()
    params = {'name': account.name, 'document': account.document}

    response = await client.post(
        BASE_PATH,
        json=params,
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['id'] is not None
    assert account.document == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_repeated_doc(client, token, session):
    account = await AccountFactory.build()

    response_original = await client.post(
        BASE_PATH,
        json={'name': account.name, 'document': account.document},
        headers={'authorization': f'Bearer {token}'},
    )

    id_object = await CRUDBase[Account](Account, session).get_one(
        response_original.json()['id']
    )
    assert id_object is not None

    params = {'name': 'Repeated Account', 'document': account.document}

    response = await client.post(
        BASE_PATH,
        json=params,
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
