# tests/domain/estates/test_estate_schema.py
import pytest

from app.domain.estates.schemas import EstateCreate

VALID_BOUNDARY = 'MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))'
VALID_POINT_INSIDE = 'POINT (0.5 0.5)'
VALID_POINT_ON_BOUNDARY = 'POINT (0 0)'
POINT_OUTSIDE = 'POINT (2 2)'
INVALID_WKT = 'NOT A WKT'
POLYGON_NOT_MULTIPOLYGON = 'POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))'


def base_data(**kwargs) -> dict:
    return {
        'label': 'Fazenda Teste',
        'slug': 'fazenda-teste',
        **kwargs,
    }


# boundary_wkt
def test_valid_boundary_wkt():
    data = EstateCreate(**base_data(boundary_wkt=VALID_BOUNDARY))
    assert data.boundary_wkt == VALID_BOUNDARY


def test_invalid_boundary_wkt_raises():
    with pytest.raises(ValueError, match='Not valid WKT'):
        EstateCreate(**base_data(boundary_wkt=INVALID_WKT))


def test_boundary_wkt_not_multipolygon_raises():
    with pytest.raises(ValueError, match='Must be a MultiPolygon'):
        EstateCreate(**base_data(boundary_wkt=POLYGON_NOT_MULTIPOLYGON))


def test_boundary_wkt_none_is_valid():
    data = EstateCreate(**base_data(boundary_wkt=None))
    assert data.boundary_wkt is None


# entrance_point_wkt
def test_valid_entrance_point_wkt():
    data = EstateCreate(
        **base_data(
            boundary_wkt=VALID_BOUNDARY,
            entrance_point_wkt=VALID_POINT_INSIDE,
        )
    )
    assert data.entrance_point_wkt == VALID_POINT_INSIDE


def test_entrance_point_on_boundary_is_valid():
    data = EstateCreate(
        **base_data(
            boundary_wkt=VALID_BOUNDARY,
            entrance_point_wkt=VALID_POINT_ON_BOUNDARY,
        )
    )
    assert data.entrance_point_wkt == VALID_POINT_ON_BOUNDARY


def test_entrance_point_outside_boundary_raises():
    with pytest.raises(ValueError, match='within or on the boundary'):
        EstateCreate(
            **base_data(
                boundary_wkt=VALID_BOUNDARY,
                entrance_point_wkt=POINT_OUTSIDE,
            )
        )


def test_entrance_point_without_boundary_is_valid():
    data = EstateCreate(
        **base_data(
            boundary_wkt=None,
            entrance_point_wkt=VALID_POINT_INSIDE,
        )
    )
    assert data.entrance_point_wkt == VALID_POINT_INSIDE


def test_invalid_entrance_point_wkt_raises():
    with pytest.raises(ValueError, match='Not valid WKT'):
        EstateCreate(
            **base_data(
                boundary_wkt=VALID_BOUNDARY,
                entrance_point_wkt=INVALID_WKT,
            )
        )


# timezone
def test_valid_timezone():
    data = EstateCreate(**base_data(timezone='America/Sao_Paulo'))
    assert data.timezone == 'America/Sao_Paulo'


def test_invalid_timezone_raises():
    with pytest.raises(ValueError, match='Invalid timezone'):
        EstateCreate(**base_data(timezone='America/Invalid'))


# slug
def test_valid_slug():
    data = EstateCreate(**base_data(slug='fazenda-teste-01'))
    assert data.slug == 'fazenda-teste-01'


def test_slug_too_short_raises():
    with pytest.raises(
        ValueError, match='String should have at least 5 characters'
    ):
        EstateCreate(**base_data(slug='abcd'))


# declared_area_m2
def test_declared_area_zero_raises():
    with pytest.raises(ValueError, match='Input should be greater than 0'):
        EstateCreate(**base_data(declared_area_m2=0))


def test_declared_area_negative_raises():
    with pytest.raises(ValueError, match='Input should be greater than 0'):
        EstateCreate(**base_data(declared_area_m2=-1))
