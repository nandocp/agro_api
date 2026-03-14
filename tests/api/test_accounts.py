from http import HTTPStatus

import pytest
from br_cpf_cnpj import generate_random_cnpj, generate_random_cpf

from app.domain.accounts.models import Account
from app.shared.crud import CRUDBase
from app.shared.utils import digits_only
from tests.factories.accounts import AccountFactory

BASE_PATH = '/api/accounts'


@pytest.mark.asyncio
async def test_create_account_without_auth_headers(client):
    account = await AccountFactory.build()
    params = {'name': account.name, 'document': account.document}

    response = await client.post(BASE_PATH, json=params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_account_with_cpf(client, token, session):
    cpf = generate_random_cpf(masked=True)
    params = {'name': 'Account CPF', 'document': cpf}

    response = await client.post(
        BASE_PATH,
        json=params,
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert cpf == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_cnpj(client, token, session):
    cnpj = generate_random_cnpj(alphanumeric=False, masked=True)
    params = {'name': 'Account CNPJ', 'document': cnpj}

    response = await client.post(
        BASE_PATH,
        json=params,
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert cnpj == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_other_doc(client, token, session):
    doc = '00.123-543/10'
    params = {'name': 'Account CPF', 'document': doc}

    response = await client.post(
        BASE_PATH,
        json=params,
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert digits_only(doc) == response.json()['document']

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
