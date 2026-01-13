# from http import HTTPStatus
# from uuid import uuid4

# import pytest

# from tests.factories.estate_plots import EstatePlotFactory
# from tests.factories.estates import EstateFactory


# @pytest.mark.asyncio
# async def test_create_estate_plot_with_unmatching_estate_id(
#     client, session, token, estate, user
# ):
#     other_estate = EstateFactory(user_id=user.id)
#     session.add(other_estate)
#     await session.commit()
#     new_plot = EstatePlotFactory.build(estate_id=estate.id)
#     plot_data = {
#         'estate_id': str(estate.id),
#         'slug': new_plot.slug,
#         'label': new_plot.label,
#         'land_use': new_plot.land_use.value,
#         'status': new_plot.status.value,
#         'limits': [
#             (-46.641, -23.551),
#             (-46.636, -23.551),
#             (-46.636, -23.546),
#             (-46.641, -23.546),
#             (-46.641, -23.551),
#         ],
#     }

#     response = client.post(
#         f'/estates/{other_estate.id}/estate_plots',
#         json=plot_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.asyncio
# async def test_create_estate_plot_with_inexisting_estate(
#     client, session, token, estate
# ):
#     inexisting_id = str(uuid4())
#     new_plot = EstatePlotFactory.build(estate_id=estate.id)
#     plot_data = {
#         'estate_id': inexisting_id,
#         'slug': new_plot.slug,
#         'label': new_plot.label,
#         'land_use': new_plot.land_use.value,
#         'status': new_plot.status.value,
#         'limits': [],
#     }

#     response = client.post(
#         f'/estates/{inexisting_id}/estate_plots',
#         json=plot_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.asyncio
# async def test_create_estate_plot_with_different_user_id(
#     client, session, token, estate, other_user
# ):
#     estate.user_id = other_user.id
#     session.add(estate)
#     await session.commit()
#     new_plot = EstatePlotFactory.build(estate_id=estate.id)
#     plot_data = {
#         'estate_id': str(estate.id),
#         'slug': new_plot.slug,
#         'label': new_plot.label,
#         'land_use': new_plot.land_use.value,
#         'status': new_plot.status.value,
#         'limits': [],
#     }

#     response = client.post(
#         f'/estates/{estate.id}/estate_plots',
#         json=plot_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED


# @pytest.mark.asyncio
# async def test_create_estate_plot_inside_estate_limit(
#     client, session, token, estate
# ):
#     new_plot = EstatePlotFactory.build(estate_id=estate.id)
#     plot_data = {
#         'estate_id': str(estate.id),
#         'slug': new_plot.slug,
#         'label': new_plot.label,
#         'land_use': new_plot.land_use.value,
#         'status': new_plot.status.value,
#         'limits': [
#             (-46.641, -23.551),
#             (-46.636, -23.551),
#             (-46.636, -23.546),
#             (-46.641, -23.546),
#             (-46.641, -23.551),
#         ],
#     }

#     response = client.post(
#         f'/estates/{estate.id}/estate_plots',
#         json=plot_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.CREATED


# # @pytest.mark.asyncio
# # async def test_create_estate_plot_inside_estate_limit(
# #     client, session, estate, token
# # ):
# #     new_estate = EstatePlotFactory(estate_id=estate.id)
# #     estate_data = {
# #         'slug': new_estate.slug,
# #         'label': new_estate.label,
# #         'opened_at': str(new_estate.opened_at),
# #         'kind': 'rural',
# #     }

# #     response = client.post(
# #         '/estates',
# #         json=estate_data,
# #         headers={'Authorization': f'Bearer {token}'},
# #     )

# #     assert response.status_code == HTTPStatus.CREATED


# # INVALID POLYGON: coords = [(0, 2), (0, 1), (2, 0), (0, 0), (0, 2)]
