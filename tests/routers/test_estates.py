from http import HTTPStatus
from secrets import token_hex

import pytest

from agro_api.entities.estate import EstateKind
from tests.factories.estates import EstateFactory


@pytest.mark.asyncio
async def test_create_estate(client, session, user, token):
    new_estate = EstateFactory(user_id=user.id)
    estate_data = {
        'slug': new_estate.slug,
        'label': new_estate.label,
        'opened_at': str(new_estate.opened_at),
        'kind': 'rural',
    }

    response = client.post(
        '/estates',
        json=estate_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    # assert response.json() == {
    #     'name': user_data['name'],
    #     'email': user_data['email'],
    #     'id': str(user_db.id),
    #     'created_at': str(user_db.created_at).replace(' ', 'T'),
    # }


@pytest.mark.asyncio
async def test_get_index_estates_without_query(
    client, token, user, session, other_user
):
    batch_size = 3
    estates = EstateFactory.create_batch(batch_size, user_id=user.id)
    session.add_all(estates)

    other_estates = EstateFactory.create_batch(
        batch_size, user_id=other_user.id
    )
    session.add_all(other_estates)
    await session.commit()

    response = client.get(
        '/estates', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['estates']) == batch_size


@pytest.mark.asyncio
async def test_get_index_estates_with_kind_query(
    client, token, user, session, other_user
):
    batch_size = 3
    rural_estates = EstateFactory.create_batch(
        batch_size, user_id=user.id, kind=EstateKind.rural
    )
    urban_estates = EstateFactory.create_batch(
        batch_size, user_id=user.id, kind=EstateKind.periurban
    )
    session.add_all(rural_estates)
    session.add_all(urban_estates)

    other_estates = EstateFactory.create_batch(
        batch_size, user_id=other_user.id
    )
    session.add_all(other_estates)
    await session.commit()

    response = client.get(
        '/estates/?kind=rural', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['estates']) == batch_size


@pytest.mark.asyncio
async def test_get_index_estates_with_slug_query(
    client, token, user, session, other_user
):
    batch_size = 3
    slug = token_hex(4)
    slug_estate = EstateFactory.create(user_id=user.id, slug=slug)
    other_estates = EstateFactory.create_batch(
        batch_size, user_id=user.id, kind=EstateKind.periurban
    )
    session.add(slug_estate)
    session.add_all(other_estates)

    other_estates = EstateFactory.create_batch(
        batch_size, user_id=other_user.id
    )
    session.add_all(other_estates)
    await session.commit()

    response = client.get(
        f'/estates/?slug={slug}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['estates']) == 1


@pytest.mark.asyncio
async def test_get_index_estates_with_label_query(
    client, token, user, session, other_user
):
    batch_size = 3
    label = EstateFactory().label
    slug_estate = EstateFactory.create_batch(
        batch_size, user_id=user.id, label=label
    )
    other_estates = EstateFactory.create_batch(batch_size, user_id=user.id)
    session.add_all(slug_estate)
    session.add_all(other_estates)

    other_estates = EstateFactory.create_batch(
        batch_size, user_id=other_user.id
    )
    session.add_all(other_estates)
    await session.commit()

    response = client.get(
        f'/estates/?label={label}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['estates']) == batch_size


@pytest.mark.asyncio
async def test_get_one_estate_with_client_token(client, token, user, session):
    estate = EstateFactory(user_id=user.id)
    estates = EstateFactory.create_batch(3, user_id=user.id)
    session.add(estate)
    session.add_all(estates)
    await session.commit()

    response = client.get(
        f'/estates/{estate.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'closed_at': None,
        'created_at': str(estate.created_at).replace(' ', 'T'),
        'id': str(estate.id),
        'kind': estate.kind.value,
        'label': estate.label,
        'opened_at': str(estate.opened_at).replace(' ', 'T'),
        'slug': estate.slug,
        'updated_at': str(estate.updated_at).replace(' ', 'T'),
        'user_id': str(estate.user_id),
    }


@pytest.mark.asyncio
async def test_update_estate_kind(client, session, user, token):
    estate = EstateFactory(user_id=user.id, kind=EstateKind.intraurban)
    session.add(estate)
    await session.commit()

    assert estate.kind.value == 'intraurban'

    closed_at = estate.closed_at
    if closed_at:
        closed_at = str(closed_at)

    estate_params = {
        'kind': EstateKind.periurban.value,
        'label': estate.label,
        'opened_at': str(estate.opened_at),
        'closed_at': closed_at,
        'slug': estate.slug
    }

    response = client.put(
        f'/estates/{estate.id}',
        json=estate_params,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert estate.kind.value == 'periurban'
