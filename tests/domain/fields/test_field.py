from datetime import datetime

import pytest

from tests.factories.fields import FieldFactory


@pytest.mark.asyncio
async def test_field_repr_(field):
    _repr = (
        f'Field(id={field.id}, '
        f'slug={field.slug}, '
        f'estate={field.estate_id}, '
        f'created_at={field.created_at})'
    )
    assert str(field) == _repr


# is_active
async def test_is_active():
    field = await FieldFactory.build()
    field.active_to = None
    assert field.is_active


async def test_is_not_active():
    field = await FieldFactory.build()
    field.active_to = datetime.now()
    assert not field.is_active
