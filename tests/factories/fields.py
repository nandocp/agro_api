import factory

from app.domain.fields.models import Field, FieldSoilClassification

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class FieldFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Field

    estate_id = None
    creator_id = None
    slug = factory.Sequence(lambda n: f'plot#{n}')
    label = Faker('word')


class FieldSoilClassification(AsyncSQLAlchemyFactory):
    class Meta:
        model = FieldSoilClassification
