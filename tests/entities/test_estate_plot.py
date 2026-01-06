import pytest

from agro_api.entities.estate_plot import EstatePlot


@pytest.mark.asyncio
async def test_estate_plot_custom__repr___without_area(estate, session):
    division = EstatePlot(
        estate_id=estate.id,
        land_use='agriculture',
        slug='div#1'
    )

    session.add(division)
    await session.commit()
    await session.refresh(division)

    attrs = [
        f'estate={division.estate.slug}',
        f'slug={division.slug}',
        f'area={division.area()}'
    ]
    assert str(division) == f'<EstatePlot({', '.join(attrs)})>'


# @pytest.mark.asyncio
# async def test_estate_plot_custom__repr___with_area(estate, session):
#     division = EstatePlot(
#         estate_id=estate.id,
#         land_use='agriculture',
#         slug='div#1'
#     )

#     session.add(division)
#     await session.commit()
#     await session.refresh(division)

#     attrs = [
#         f'estate={division.estate.slug}',
#         f'slug={division.slug}',
#         f'area={division.area()}'
#     ]
#     assert str(division) == f'<EstatePlot({', '.join(attrs)})>'
