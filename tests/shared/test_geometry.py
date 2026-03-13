from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon, Point, Polygon

from app.shared.geometry import (
    EPSG,
    shape_to_wkb,
    to_geojson,
    to_geometry,
    wkb_to_shape,
)

# fixtures
POINT = Point(1.0, 2.0)
POLYGON = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
MULTIPOLYGON = MultiPolygon([POLYGON])
POINT_GEOJSON = {'type': 'Point', 'coordinates': (1.0, 2.0)}
POLYGON_GEOJSON = {
    'type': 'Polygon',
    'coordinates': (((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)),),
}


# shape_to_wkb
def test_shape_to_wkb_from_base_geometry():
    result = shape_to_wkb(POINT)
    assert isinstance(result, WKBElement)


def test_shape_to_wkb_from_wkb_element():
    wkb = from_shape(POINT, srid=EPSG.WGS84.value)
    result = shape_to_wkb(wkb)
    assert result is wkb


def test_shape_to_wkb_none_returns_none():
    assert shape_to_wkb(None) is None


def test_shape_to_wkb_custom_srid():
    result = shape_to_wkb(POINT, srid=EPSG.WEBM)
    assert isinstance(result, WKBElement)


# wkb_to_shape
def test_wkb_to_shape_from_wkb_element():
    wkb = from_shape(POINT, srid=EPSG.WGS84.value)
    result = wkb_to_shape(wkb)
    assert isinstance(result, Point)
    assert result.equals(POINT)


def test_wkb_to_shape_from_base_geometry():
    result = wkb_to_shape(POINT)
    assert result is POINT


def test_wkb_to_shape_none_returns_none():
    assert wkb_to_shape(None) is None


# to_geometry
def test_to_geometry_none_returns_none():
    assert to_geometry(None) is None


def test_to_geometry_from_base_geometry():
    result = to_geometry(POINT)
    assert result is POINT


def test_to_geometry_from_wkb_element():
    wkb = from_shape(POINT, srid=EPSG.WGS84.value)
    result = to_geometry(wkb)
    assert isinstance(result, Point)


def test_to_geometry_from_list():
    result = to_geometry([1.0, 2.0])
    assert isinstance(result, Point)
    assert result.equals(POINT)


def test_to_geometry_from_list_invalid_length():
    assert to_geometry([1.0]) is None
    assert to_geometry([1.0, 2.0, 3.0]) is None


def test_to_geometry_from_geojson_point():
    result = to_geometry(POINT_GEOJSON)
    assert isinstance(result, Point)


def test_to_geometry_from_geojson_polygon():
    result = to_geometry(POLYGON_GEOJSON)
    assert isinstance(result, Polygon)


def test_to_geometry_from_geo_interface():
    class FakeGeom:
        __geo_interface__ = POINT_GEOJSON

    result = to_geometry(FakeGeom())
    assert isinstance(result, Point)


def test_to_geometry_invalid_type_returns_none():
    assert to_geometry('invalid') is None
    assert to_geometry(42) is None


# to_geojson
def test_to_geojson_none_returns_none():
    assert to_geojson(None) is None


def test_to_geojson_from_dict():
    result = to_geojson(POINT_GEOJSON)
    assert result is POINT_GEOJSON


def test_to_geojson_from_base_geometry_point():
    result = to_geojson(POINT)
    assert result['type'] == 'Point'
    assert result['coordinates'] == (1.0, 2.0)


def test_to_geojson_from_base_geometry_polygon():
    result = to_geojson(POLYGON)
    assert result['type'] == 'Polygon'


def test_to_geojson_from_wkb_element():
    wkb = from_shape(POINT, srid=EPSG.WGS84.value)
    result = to_geojson(wkb)
    assert result['type'] == 'Point'
