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
