from datetime import datetime

import factory
from geoalchemy2.shape import from_shape
from shapely import geometry

from app.domain.estates.models import Estate

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


"""
Polygon orientation: Points should be listed in counter-clockwise order.
If you list them clockwise, PostGIS will interpret it as a "hole"
(a negative area).

Closing the polygon: The first and last points must be the same
to close the shape.

Coordinate order: Always longitude first, then latitude
in WKT format and in Shapely.
"""
polygon = geometry.Polygon([
    (-45.8923, -21.7342),  # Ponto 1 (NW) (lon, lat)
    (-45.8745, -21.7342),  # Ponto 2 (NE)
    (-45.8621, -21.7428),  # Ponto 3
    (-45.8512, -21.7584),  # Ponto 4
    (-45.8478, -21.7741),  # Ponto 5
    (-45.8523, -21.7895),  # Ponto 6
    (-45.8656, -21.7982),  # Ponto 7
    (-45.8842, -21.8015),  # Ponto 8
    (-45.8978, -21.7956),  # Ponto 9
    (-45.9034, -21.7832),  # Ponto 10
    (-45.9021, -21.7654),  # Ponto 11
    (-45.8967, -21.7512),  # Ponto 12
    (-45.8923, -21.7342),  # Fecha o polígono
])
point = geometry.Point(-45.8876, -21.7389)


class EstateFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Estate

    opened_at = factory.LazyFunction(datetime.now)
    label = Faker('word')
    slug = factory.Sequence(lambda n: f'estate#{n}')
    description = Faker('sentence')
    boundary = from_shape(polygon, srid=4326)
    entrance_point = from_shape(point, srid=4326)
    declared_area_m2 = 1800000
    account_id = None
