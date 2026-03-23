import pytest

from tests.factories.fields import SoilClassificationFactory


@pytest.mark.asyncio
async def test_soil_classification_repr_():
    classification = await SoilClassificationFactory.build()

    tester = [f'name={classification.name}', f'source={classification.source}']

    assert str(classification) == f'SoilClassification({(", ").join(tester)})'
