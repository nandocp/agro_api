from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from agro_api.entities.estate import Estate, EstateKind
from tests.factories.estates import EstateFactory


def test_is_urban_true_with_periurban():
    estate = EstateFactory(kind=EstateKind.PERIURBAN)

    assert estate.is_urban


def test_is_urban_true_with_intraurban():
    estate = EstateFactory(kind=EstateKind.INTRAURBAN)

    assert estate.is_urban


def test_is_urban_false():
    estate = EstateFactory(kind=EstateKind.RURAL)

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
    new_estate = Estate(
        account_id=estate.account_id,
        label='Test2',
        slug=estate.slug,
        account=estate.account,
        opened_at=datetime.now(),
    )
    session.add(new_estate)

    err_message = (
        'duplicate key value violates '
        'unique constraint "idx_account_estate_slug"'
    )
    with pytest.raises(IntegrityError, match=err_message):
        await session.commit()

    # # Same slug, different account - should succeed
    # account2 = Account(...)
    # Estate(account_id=account2.id, label='Test3', slug='same')
    # db_session.commit()  # Should work
