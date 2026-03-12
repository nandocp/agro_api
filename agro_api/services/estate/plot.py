# from datetime import datetime
# from typing import List, Optional

# from sqlalchemy.exc import IntegrityError

# from agro_api.entities.estate import Estate, Plot
# from agro_api.repositories.estate import EstateRepository
# from agro_api.services.base import BaseService
# from config.http_misc import unauthorized, unprocessable


# class PlotService(BaseService):
#     async def create(self, create_params, estate_id) -> Plot:
#         # 0. Verify if estate_id's are matching
#         if not str(create_params.estate_id) == estate_id:
#             unauthorized()

#         find_params = {'id': estate_id, 'user_id': self.user.id}
#         estate = await EstateRepository(
#             session=self.session, model=Estate
#         ).get_by(find_params)

#         # 1. A User can only create Plots on Estates owned by them
#         if not estate:
#             unauthorized()

#         if not create_params.slug:
#             now = datetime.now()
#             now.strftime('')
#             create_params.slug = f'plot#{now.strftime("%Y%m%d%H%M%S")}'

#         try:
#             return await self.repository.create(obj_in=create_params)
#         except IntegrityError:
#             unprocessable('Plot.slug already exists')

#     async def get_by_id(
#         self, *, estate_id: str, plot_id: int
#     ) -> Optional[Plot]:
#         params = {'id': plot_id, 'estate_id': estate_id}
#         return await self.repository.get_by(params)

#     async def get_list(self, filters, estate_id) -> List[Plot]:
#         if not estate_id:
#             unprocessable('Missing estate_id')

#         sanitized_filters = BaseService.sanitize_filters(filters)
#         sanitized_filters['estate_id'] = estate_id
#         return await self.repository.get_many(sanitized_filters)

#     def update(self, *, obj_id: str, obj_in) -> Plot:
#         pass  # pragma: no cover

#     def remove(self, *, id: int) -> None:
#         pass  # pragma: no cover

# # from config.geometry import
# # from config.geometry import
# # create_polygon_geometry,
# # shape_to_wkb,
# # wkb_to_shapecreate_polygon_geometry,
# # shape_to_wkb, wkb_to_shape
# # from shapely.validation import explain_validity

#         # # 2. A Plot must not be placed outside the limits of a Estate
#         # verify_limits(estate, create_params)

#         # active_params = {'estate_id': estate_id, 'status': 'active'}
#         # active_plots = await self.repository.get_by(active_params)
#         # limits = create_params.limits
#         # breakpoint()
#         # if limits:
#         #     limits = create_polygon_geometry(limits)

#         #     # 3. A new Plot cannot overlap other active Plots
#         #     if any(limits.intersect(plot.limits) for plot in active_plots):
#         #         unprocessable('Plot is overlaping')
#         # elif estate.limits and len(active_plots) == 0:
#         #     # 4. If params has no limits AND estate has no active Plot
#         #     limits = wkb_to_shape(estate.limits)

#         # if limits and not limits.is_valid:
#         #     unprocessable(explain_validity(limits))

#         # create_params.limits = shape_to_wkb(limits)


# # def verify_limits(estate, plot):
# #     estate_limits = wkb_to_shape(estate.limits)
# #     plot_limits = wkb_to_shape(plot.limits)

# #     limits_present = estate_limits and plot_limits
# #     plot_inside_estate = estate_limits.contains(plot_limits)

# #     if limits_present and not plot_inside_estate:
# #         unprocessable('Plot not inside Estate limits')

# #     return True
