from typing import Any

import geoalchemy2.shape
from geoalchemy2 import WKBElement
from shapely import wkt
from shapely.geometry import MultiPolygon, Point, Polygon, shape
from shapely.geometry.base import BaseGeometry
from shapely.validation import explain_validity

from app.shared.enums import EPSG


def shape_to_wkb(
    value: BaseGeometry | WKBElement, srid: EPSG = EPSG.WGS84
) -> WKBElement | None:
    if isinstance(value, BaseGeometry):
        return geoalchemy2.shape.from_shape(value, srid=srid.value)
    if isinstance(value, WKBElement):
        return value
    return None


def wkb_to_shape(value: WKBElement | BaseGeometry) -> BaseGeometry | None:
    if isinstance(value, WKBElement):
        return geoalchemy2.shape.to_shape(value)
    if isinstance(value, BaseGeometry):
        return value
    return None


def wkt_to_wkb(value: str, srid: EPSG = EPSG.WGS84) -> WKBElement:
    """Convenience — parse WKT string directly to WKBElement."""
    return shape_to_wkb(wkt.loads(value), srid=srid)


def to_geometry(value: Any) -> BaseGeometry | None:
    LAT_LON = 2
    if value is None:
        return None
    if isinstance(value, WKBElement):
        return wkb_to_shape(value)
    if isinstance(value, BaseGeometry):
        return value
    if isinstance(value, list) and len(value) == LAT_LON:
        value = Point(*value)
    elif isinstance(value, dict):
        value = shape(value)
    elif hasattr(value, '__geo_interface__'):
        value = shape(value.__geo_interface__)

    return value if isinstance(value, BaseGeometry) else None


def to_geojson(value: WKBElement | BaseGeometry | None) -> dict | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    geom = wkb_to_shape(value)

    return getattr(geom, '__geo_interface__', None)


def validate_multipolygon_wkt(value: str) -> str:
    try:
        geom = wkt.loads(value)
    except Exception:
        raise ValueError('Not valid WKT')
    if not isinstance(geom, MultiPolygon):
        raise ValueError('Must be a MultiPolygon')
    if not geom.is_valid:
        raise ValueError(f'Invalid geometry: {explain_validity(geom)}')
    return value


def validate_polygon_wkt(value: str) -> str:
    try:
        geom = wkt.loads(value)
    except Exception:
        raise ValueError('Not valid WKT')
    if not isinstance(geom, Polygon):
        raise ValueError('Must be a Polygon')
    if not geom.is_valid:
        raise ValueError(f'Invalid geometry: {explain_validity(geom)}')
    return value


def validate_point_wkt(value: str) -> str:
    try:
        geom = wkt.loads(value)
    except Exception:
        raise ValueError('Not valid WKT')
    if not isinstance(geom, Point):
        raise ValueError('Must be a Point')
    return value


def validate_point_within_boundary(point_wkt: str, boundary_wkt: str) -> None:
    point = wkt.loads(point_wkt)
    boundary = wkt.loads(boundary_wkt)
    if not boundary.contains(point) and not boundary.touches(point):
        raise ValueError('Point must be within or on the boundary')
