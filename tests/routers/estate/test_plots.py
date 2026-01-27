from http import HTTPStatus
from random import choice
from uuid import uuid4

import pytest

from tests.factories.estates import EstateFactory, PlotFactory


@pytest.mark.asyncio
async def test_create_plot_with_unmatching_estate_id(
    client, session, token, plot_params, user
):
    breakpoint()
    other_estate = EstateFactory(user_id=user.id)
    session.add(other_estate)
    await session.commit()

    response = client.post(
        f'/estates/{other_estate.id}/plots',
        json=plot_params,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_plot_with_inexisting_estate(
    client, session, token, plot_params
):
    inexisting_id = str(uuid4())
    plot_params['estate_id'] = inexisting_id

    response = client.post(
        f'/estates/{inexisting_id}/plots',
        json=plot_params,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_plot_with_different_user_id(
    client, session, token, estate, other_user
):
    estate.user_id = other_user.id
    session.add(estate)
    await session.commit()

    new_plot = PlotFactory.build(estate_id=estate.id)
    plot_data = {
        'estate_id': str(estate.id),
        'slug': new_plot.slug,
        'label': new_plot.label,
        'land_use': new_plot.land_use.value,
        'status': new_plot.status.value,
        'created_by': str(other_user.id)
    }

    response = client.post(
        f'/estates/{estate.id}/plots',
        json=plot_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_plot_success(
    client, session, token, plot_params
):
    response = client.post(
        f'/estates/{plot_params['estate_id']}/plots',
        json=plot_params,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_plot_with_repeated_slug(
    client, session, estate, token, plot
):
    params = PlotFactory(estate_id=estate.id)
    estate_data = {
        'slug': plot.slug,
        'label': params.label,
        'estate_id': str(params.estate_id),
        'land_use': params.land_use,
        'created_by': str(params.created_by),
        'status': params.status
    }

    response = client.post(
        f'/estates/{estate.id}/plots',
        json=estate_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json()['detail'] == 'Plot.slug already exists'


@pytest.mark.asyncio
async def test_show_plot(
    client, session, token, plot
):
    response = client.get(
        f'/estates/{plot.estate_id}/plots/{plot.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == str(plot.id)
    assert response.json()['estate_id'] == str(plot.estate_id)


@pytest.mark.asyncio
async def test_show_plots(client, session, token, estate, user):
    batch = 5
    plots = PlotFactory.create_batch(
        batch, estate_id=estate.id, created_by=user.id
    )
    session.add_all(plots)
    await session.commit()

    response = client.get(
        f'/estates/{estate.id}/plots',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['plots']) == batch


@pytest.mark.asyncio
async def test_show_only_estate_id_plots(
    client, session, token, estate, user
):
    batch = 5
    active = PlotFactory.create_batch(
        batch, estate_id=estate.id, created_by=user.id
    )
    status = PlotFactory.create_batch(
        batch,
        estate_id=estate.id,
        created_by=user.id,
        status=choice(['inactive', 'merged', 'divided'])
    )
    session.add_all([*active, *status])
    await session.commit()

    response = client.get(
        f'/estates/{estate.id}/plots/?status=active',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['plots']) == batch


@pytest.mark.asyncio
async def test_show_active_plots(client, session, token, estate, user):
    batch = 5
    active = PlotFactory.create_batch(
        batch, estate_id=estate.id, created_by=user.id, status='active'
    )
    status = PlotFactory.create_batch(
        batch,
        estate_id=estate.id,
        created_by=user.id,
        status=choice(['inactive', 'merged', 'divided'])
    )
    session.add_all([*active, *status])
    await session.commit()

    response = client.get(
        f'/estates/{estate.id}/plots/?status=active',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['plots']) == batch
