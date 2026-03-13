from enum import Enum
from typing import Any

import geoalchemy2.shape
from geoalchemy2 import WKBElement
from shapely.geometry import Point, shape
from shapely.geometry.base import BaseGeometry


class EPSG(int, Enum):
    WGS84 = 4326
    WEBM = 3857


class GeometrySource(str, Enum):
    survey = 'survey'
    satellite = 'satellite'
    manual = 'manual'
    imported = 'imported'


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
