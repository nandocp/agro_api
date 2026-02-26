# https://gist.github.com/la-mar/439bb675ea84a2bac308de1e35c37fa5

from enum import Enum

# import logging
# from typing import Dict, Optional, Union

# from geoalchemy2 import WKBElement
# from geoalchemy2.shape import from_shape, to_shape
# from shapely import set_srid
# from shapely.geometry import Point, Polygon, shape
# from shapely.geometry.base import BaseGeometry

# logger = logging.getLogger(__name__)

# WKT: Well Known Text
# WKB: how data is stored in the database
# Polygon / Point: how data is manipulated by python / shapely


class GeometrySource(str, Enum):
    survey = 'survey'
    satellite = 'satellite'
    manual = 'manual'
    imported = 'imported'


# class EPSG(int, Enum):
#     WGS84 = 4326
#     WEBM = 3857  # web-mercator: projected from WGS84
#     SIRGAS2000 = 31983

#     ALT = 4979


# def transform_point(raw_coordinates):
#     if not raw_coordinates:
#         return None

#     coord_as_point = Point(raw_coordinates)
#     return from_shape(coord_as_point, srid=4326)


# def transform_polygon(raw_limits):
#     if not raw_limits:
#         return None

#     limits_as_polygon = Polygon(raw_limits)
#     return from_shape(limits_as_polygon, srid=4326)


# def shape_to_wkb(
#     shape: Union[BaseGeometry, WKBElement], srid: EPSG = EPSG.WGS84
# ) -> Optional[WKBElement]:
#     if isinstance(shape, BaseGeometry):
#         return from_shape(shape, srid=EPSG(srid).value)
#     elif isinstance(shape, WKBElement):
#         return shape
#     else:
#         return None


# def wkb_to_shape(
#     wkb: Union[WKBElement, BaseGeometry],
# ) -> Optional[BaseGeometry]:
#     if isinstance(wkb, WKBElement):
#         return to_shape(wkb)
#     elif isinstance(wkb, BaseGeometry):
#         return wkb
#     else:
#         return None


# def area_from_wkb(
#     wkb: Union[WKBElement, BaseGeometry],
#     srid: EPSG = EPSG.SIRGAS2000,
#     formatter: int = None,
# ) -> float:
#     if not wkb:
#         return None

#     shape = wkb_to_shape(wkb)
#     area = shape_to_area(shape, srid)
#     if not formatter:
#         return area

#     formatter = f'{formatter}f'
#     formatted_area = f'{area:.{formatter}}'
#     return float(formatted_area)


# def shape_to_area(
# shape: BaseGeometry, srid: EPSG = EPSG.SIRGAS2000) -> float:
#     return set_srid(shape, srid).area


# def create_polygon_geometry(v) -> Polygon | None:
#     if not v:
#         return None

#     try:
#         if isinstance(v, list):
#             return Polygon(v)
#         elif isinstance(v, dict):
#             return shape(v)
#         elif hasattr(v, '__geo_interface__'):
#             pass  # v is already a geometry

#         return v
#     except Exception as e:
#         logger.debug(f'Failed creating Polygon geometry: v={v} -- {e}')


# def create_point_geometry(v) -> Point:
#     if not v:
#         return None

#     try:
#         if isinstance(v, list):
#             return Point(*v)
#         elif isinstance(v, dict):
#             return shape(v)
#         elif hasattr(v, '__geo_interface__'):
#             pass  # v is already a geometry
#         return v
#     except Exception as e:
#         logger.debug(f'Failed creating Point geometry: v={v} -- {e}')


# def dump_geometry(cls, v) -> Dict:
#     if isinstance(v, dict):
#         return v

#     return getattr(wkb_to_shape(v), '__geo_interface__', None)

    # @hybrid_property
    # def perimeter_m(self) -> float | None:
    #     """Calculate perimeter in meters"""
    #     if self.boundary is None:
    #         return None
    #     # Transform to UTM for meter-accurate measurement
    #     return db.session.scalar(
    #         select(func.ST_Perimeter(
    # func.ST_Transform(self.boundary, self._get_utm_srid())))
    #     )

    # @perimeter_m.expression
    # def perimeter_m(cls):
    #     """Database-side expression for querying/filtering"""
    #     return func.ST_Perimeter(f
    # unc.ST_Transform(cls.boundary, self._get_utm_srid()))

    # @hybrid_property
    # def area_ha(self):
    #     return func.ST_Area(func.ST_Transform(self.boundary, 3857)) / 10000

    # @area_ha.expression
    # def area_ha(cls):
    #     return func.ST_Area(func.ST_Transform(cls.boundary, 3857)) / 10000
