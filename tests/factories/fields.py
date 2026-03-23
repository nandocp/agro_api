from datetime import date

import factory

from app.domain.fields.models import (
    Field,
    FieldSoilAnalysis,
    SoilClassification,
)

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class FieldFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Field

    estate_id = None
    creator_id = None
    slug = factory.Sequence(lambda n: f'plot#{n}')
    label = Faker('word')


class SoilClassificationFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = SoilClassification

    name = Faker('word')
    source = Faker('word')


class FieldSoilAnalysis(AsyncSQLAlchemyFactory):
    class Meta:
        model = FieldSoilAnalysis

    collected_at = date.today()
    collector_name = Faker('word')
    collector_registry = Faker('word')
    laboratory_name = Faker('word')
