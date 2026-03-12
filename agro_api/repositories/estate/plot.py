# from sqlalchemy import func, select

# from agro_api.entities.estate import Estate
# from agro_api.entities.plot import Plot
# from agro_api.repositories.base import BaseRepository

# # from agro_api.schemas.estate import PlotCreate, PlotUpdate


# class PlotRepository(BaseRepository):
#     # class PlotRepository(BaseRepository[Plot, PlotCreate, PlotUpdate]):
#     async def _validate_plot_boundary(self, plot: Plot):
#         """Validate plot boundary is within estate boundary."""
#         if plot.boundary is None:
#             return

#         # Get estate boundary
#         result = await self.session.execute(
#             select(Estate.boundary).where(Estate.id == plot.estate_id)
#         )
#         estate_boundary = result.scalar_one_or_none()

#         if estate_boundary is None:
#             raise ValueError("Estate has no boundary defined")

#         # Check containment
#         result = await self.session.execute(
#             select(func.ST_Within(plot.boundary, estate_boundary))
#         )
#         is_within = result.scalar()

#         if not is_within:
#             raise ValueError("Plot boundary must be within estate boundary")
