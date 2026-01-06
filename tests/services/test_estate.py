from agro_api.services.estate import EstateService


def test_transform_none_coordinates():
    assert not EstateService.transform_coordinates(None)


def test_transform_none_limits():
    assert not EstateService.transform_limits(None)
