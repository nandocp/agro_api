from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.estates.enums import EstateKind
from tests.factories.accounts import AccountFactory
from tests.factories.estates import EstateFactory


@pytest.mark.asyncio
async def test_is_urban_true_with_periurban():
    estate = await EstateFactory.build(kind=EstateKind.PERIURBAN)

    assert estate.is_urban


@pytest.mark.asyncio
async def test_is_urban_true_with_intraurban():
    estate = await EstateFactory.build(kind=EstateKind.INTRAURBAN)

    assert estate.is_urban


@pytest.mark.asyncio
async def test_is_urban_false():
    estate = await EstateFactory.build(kind=EstateKind.RURAL)

    assert not estate.is_urban


@pytest.mark.asyncio
async def test_estate_repr_(estate):
    repr_attrs = [
        f'id={estate.id}',
        f'slug={estate.slug}',
        f'status={estate.status.value}',
        f'created_at={estate.created_at}',
    ]
    assert str(estate) == f'Estate({", ".join(repr_attrs)})'


@pytest.mark.asyncio
async def test_perimeter_m_compute(estate):
    test = estate.perimeter_m
    assert test is not None
    assert isinstance(test, Decimal)


@pytest.mark.asyncio
async def test_calculated_area_m2_compute(estate):
    test = estate.calculated_area_m2
    assert test is not None
    assert isinstance(test, Decimal)


@pytest.mark.asyncio
async def test_account_slug_uniqueness(session, estate):
    estate_with_error = await EstateFactory.build(
        account_id=estate.account_id, slug=estate.slug
    )
    session.add(estate_with_error)

    err_message = (
        'duplicate key value violates '
        'unique constraint "idx_account_estate_slug"'
    )
    with pytest.raises(IntegrityError, match=err_message):
        await session.commit()


@pytest.mark.asyncio
async def test_other_account_estate_same_slug(session, estate):
    account = await AccountFactory.create(session)
    new_estate = await EstateFactory.build(
        account_id=account.id, slug=estate.slug
    )
    session.add(new_estate)
    await session.commit()
