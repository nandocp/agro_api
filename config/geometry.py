# https://gist.github.com/la-mar/439bb675ea84a2bac308de1e35c37fa5

import logging
from enum import Enum
from typing import Dict, Optional, Union

from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point, Polygon, shape
from shapely.geometry.base import BaseGeometry

logger = logging.getLogger(__name__)


class EPSG(int, Enum):
    WGS84 = 4326
    WEBM = 3857  # web-mercator: projected from WGS84


def transform_point(raw_coordinates):
    if not raw_coordinates:
        return None

    coord_as_point = Point(raw_coordinates)
    return from_shape(coord_as_point, srid=4326)


def transform_polygon(raw_limits):
    if not raw_limits:
        return None

    limits_as_polygon = Polygon(raw_limits)
    return from_shape(limits_as_polygon, srid=4326)


def shape_to_wkb(
    shape: Union[BaseGeometry, WKBElement],
    srid: EPSG = EPSG.WGS84
) -> Optional[WKBElement]:
    if isinstance(shape, BaseGeometry):
        return from_shape(shape, srid=EPSG(srid).value)
    elif isinstance(shape, WKBElement):
        return shape
    else:
        return None


def wkb_to_shape(
    wkb: Union[WKBElement, BaseGeometry]
) -> Optional[BaseGeometry]:
    if isinstance(wkb, WKBElement):
        return to_shape(wkb)
    elif isinstance(wkb, BaseGeometry):
        return wkb
    else:
        return None


def create_polygon_geometry(v) -> Polygon:
    if not v:
        return None

    try:
        if isinstance(v, list):
            return Polygon(*v)
        elif isinstance(v, dict):
            return shape(v)
        elif hasattr(v, '__geo_interface__'):
            pass  # v is already a geometry

        return v
    except Exception as e:
        logger.debug(f'Failed creating Polygon geometry: v={v} -- {e}')


def create_point_geometry(v) -> Point:
    if not v:
        return None

    try:
        if isinstance(v, list):
            return Point(*v)
        elif isinstance(v, dict):
            return shape(v)
        elif hasattr(v, '__geo_interface__'):
            pass  # v is already a geometry
        return v
    except Exception as e:
        logger.debug(f'Failed creating Point geometry: v={v} -- {e}')


def dump_geometry(cls, v) -> Dict:
    if isinstance(v, dict):
        return v

    return getattr(wkb_to_shape(v), '__geo_interface__', None)
