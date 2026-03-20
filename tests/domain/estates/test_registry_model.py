import pytest

from app.domain.estates.enums import RegistryStatus
from tests.factories.estates import EstateRegistryFactory


@pytest.mark.asyncio
async def test_repr_(session, estate):
    registry = await EstateRegistryFactory.create(session, estate_id=estate.id)
    repr_attrs = [
        f'estate={registry.estate_id}',
        f'source={registry.source}',
        f'code={registry.code}',
    ]
    assert str(registry) == f'EstateRegistry({", ".join(repr_attrs)})'


@pytest.mark.asyncio
async def test_is_active(estate):
    registry = await EstateRegistryFactory.build(
        estate_id=estate.id, status=RegistryStatus.ACTIVE
    )
    assert registry.is_active


@pytest.mark.asyncio
async def test_is_not_active(estate):
    registry = await EstateRegistryFactory.build(
        estate_id=estate.id, status=RegistryStatus.CANCELLED
    )
    assert not registry.is_active
