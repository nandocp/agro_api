from http import HTTPStatus
from uuid import uuid7

import pytest
from br_cpf_cnpj import generate_random_cnpj, generate_random_cpf

from app.domain.accounts.auth import create_access_token
from app.domain.accounts.enums import AccountPlan
from app.domain.accounts.models import Account
from app.shared.crud import CRUDBase
from app.shared.utils import digits_only
from tests.factories.accounts import AccountFactory, UserFactory

SYSTEM_PATH = '/system/accounts'


@pytest.mark.asyncio
async def test_list_accounts_without_filters(client, session, superuser_token):
    await AccountFactory.create_batch(20, session=session)
    response = await client.get(
        SYSTEM_PATH, headers={'authorization': f'Bearer {superuser_token}'}
    )

    assert response.status_code == HTTPStatus.OK


async def test_list_accounts_filter_by_plan(client, session, superuser_token):
    await AccountFactory.create(session, plan=AccountPlan.FREE)
    await AccountFactory.create(session, plan=AccountPlan.PRO)
    await session.flush()

    response = await client.get(
        SYSTEM_PATH,
        params={'plan': 'free'},
        headers={'authorization': f'Bearer {superuser_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']
    assert all(a['plan'] == 'free' for a in data)


async def test_list_accounts_filter_by_name(client, session, superuser_token):
    await AccountFactory.create(session, name='Fazenda Alpha')
    await AccountFactory.create(session, name='Fazenda Beta')
    await session.flush()

    response = await client.get(
        SYSTEM_PATH,
        params={'name': 'Alpha'},
        headers={'authorization': f'Bearer {superuser_token}'},
    )
    data = response.json()['data']
    assert len(data) == 1
    assert data[0]['name'] == 'Fazenda Alpha'


async def test_list_accounts_pagination(client, session, superuser_token):
    await AccountFactory.create_batch(5, session=session)
    await session.flush()

    limit = 2
    response = await client.get(
        SYSTEM_PATH,
        params={'limit': limit, 'offset': 0},
        headers={'authorization': f'Bearer {superuser_token}'},
    )
    body = response.json()
    assert len(body['data']) == limit
    assert body['has_next'] is True
    assert body['has_previous'] is False


@pytest.mark.asyncio
async def test_create_account_without_auth_headers(client):
    response = await client.post(SYSTEM_PATH, json={}, headers={})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_account_with_incorrect_auth_headers(client):
    token = create_access_token(sub=uuid7(), jti=uuid7())

    response = await client.post(
        SYSTEM_PATH,
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_account_with_cpf(client, superuser_token, session):
    cpf = generate_random_cpf(masked=True)
    params = {'name': 'Account CPF', 'document': cpf}

    response = await client.post(
        SYSTEM_PATH,
        json=params,
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert cpf == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_cnpj(client, superuser_token, session):
    cnpj = generate_random_cnpj(alphanumeric=False, masked=True)
    params = {'name': 'Account CNPJ', 'document': cnpj}

    response = await client.post(
        SYSTEM_PATH,
        json=params,
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert cnpj == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_other_doc(client, superuser_token, session):
    doc = '00.123-543/10'
    params = {'name': 'Account CPF', 'document': doc}

    response = await client.post(
        SYSTEM_PATH,
        json=params,
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert digits_only(doc) == response.json()['document']

    id_object = await CRUDBase[Account](Account, session).get_one(
        response.json()['id']
    )
    assert id_object is not None


@pytest.mark.asyncio
async def test_create_account_with_repeated_doc(
    client, superuser_token, session
):
    account = await AccountFactory.build()

    response_original = await client.post(
        SYSTEM_PATH,
        json={'name': account.name, 'document': account.document},
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    id_object = await CRUDBase[Account](Account, session).get_one(
        response_original.json()['id']
    )
    assert id_object is not None

    params = {'name': 'Repeated Account', 'document': account.document}

    response = await client.post(
        SYSTEM_PATH,
        json=params,
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.asyncio
async def test_update_account_plan_with_no_superuser(client, account, token):
    response = await client.patch(
        f'{SYSTEM_PATH}/{account.id}/plan',
        json={},
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_update_account_plan_with_superuser(
    client, account, superuser_token
):
    assert account.plan == AccountPlan.FREE
    new_plan = AccountPlan.ENTERPRISE.value

    response = await client.patch(
        f'{SYSTEM_PATH}/{account.id}/plan',
        json={'plan': new_plan},
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    test_response = await client.get(
        f'{SYSTEM_PATH}/{account.id}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert test_response.json()['plan'] == new_plan


@pytest.mark.asyncio
async def test_update_account_plan_with_wrong_id(client, superuser_token):
    response = await client.patch(
        f'{SYSTEM_PATH}/{uuid7()}/plan',
        json={'plan': AccountPlan.PRO.value},
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_account(client, account, superuser_token):
    assert account.plan == AccountPlan.FREE

    response = await client.get(
        f'{SYSTEM_PATH}/{account.id}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_account_with_wrong_id(client, account, superuser_token):
    assert account.plan == AccountPlan.FREE

    response = await client.get(
        f'{SYSTEM_PATH}/{uuid7()}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_archive_account(client, account, superuser_token):
    response = await client.patch(
        f'{SYSTEM_PATH}/{account.id}/archive',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_archive_account_persists(
    client, account, superuser_token, session
):
    await client.patch(
        f'{SYSTEM_PATH}/{account.id}/archive',
        headers={'authorization': f'Bearer {superuser_token}'},
    )
    await session.flush()
    session.expire(account)
    await session.refresh(account)
    assert account.archived_at is not None


@pytest.mark.asyncio
async def test_archive_incorrect_account(client, session, superuser_token):
    response = await client.patch(
        f'{SYSTEM_PATH}/{uuid7()}/archive',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_account(client, superuser_token, account):
    response = await client.delete(
        f'{SYSTEM_PATH}/{account.id}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_incorrect_account(client, superuser_token):
    response = await client.delete(
        f'{SYSTEM_PATH}/{uuid7()}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_correctly_delete_account(client, session, superuser_token):
    account = await AccountFactory.create(session)
    await client.delete(
        f'{SYSTEM_PATH}/{account.id}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    test_response = await client.get(
        f'{SYSTEM_PATH}/{account.id}',
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert test_response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_create_account_user(client, superuser_token, account):
    user = await UserFactory.build()

    response = await client.post(
        f'{SYSTEM_PATH}/{account.id}/users',
        json={
            'name': user.name,
            'email': user.email,
        },
        headers={'authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
