import pytest

from tests.factories.fields import FieldSoilAnalysis


@pytest.mark.asyncio
async def test_field_soil_analysis_repr_(field):
    analysis = await FieldSoilAnalysis.build(field_id=field.id)

    tester = [
        f'field={analysis.field_id}',
        f'collected_at={analysis.collected_at}',
        f'analyzed_at={analysis.analyzed_at}',
    ]

    assert str(analysis) == f'FieldSoilAnalysis({(", ").join(tester)})'
