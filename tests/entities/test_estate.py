import pytest

from agro_api.entities.estate import EstateKind
from tests.factories.estates import EstateFactory


def test_is_urban_true_with_periurban(session, user):
    estate = EstateFactory(user_id=user.id, kind=EstateKind.periurban)

    assert estate.is_urban()


def test_is_urban_true_with_intraurban(session, user):
    estate = EstateFactory(user_id=user.id, kind=EstateKind.intraurban)

    assert estate.is_urban()


def test_is_urban_false(session, user):
    estate = EstateFactory(user_id=user.id, kind=EstateKind.rural)

    assert not estate.is_urban()


def test_area_with_limits(estate):
    assert estate.area() == '0.04'


@pytest.mark.asyncio
async def test_area_without_limits(estate, session):
    estate.limits = None
    session.add(estate)
    await session.commit()
    await session.refresh(estate)

    assert not estate.area()


def test_custom__repr__(estate):
    assert str(estate) == f'<Estate(slug={estate.slug}, area={estate.area()})>'
