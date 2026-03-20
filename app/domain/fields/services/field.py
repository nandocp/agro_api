from app.shared.service import BaseService


# from geoalchemy2.shape import from_shape
# from shapely import geometry
class FieldService(BaseService):
    pass

    # boundary = from_shape(boundary, srid=4326)


# boundary = geometry.Polygon([
#     (-45.8923, -21.7342),
#     (-45.8821, -21.7342),
#     (-45.8821, -21.7456),
#     (-45.8876, -21.7512),
#     (-45.8967, -21.7512),
#     (-45.8967, -21.7423),
#     (-45.8923, -21.7342),
# ])


# """
# # Talhão 1: Café - 45 hectares (Melhor solo, meia encosta)
# talhao1_polygon = Polygon([
#     (-45.8923, -21.7342),
#     (-45.8821, -21.7342),
#     (-45.8821, -21.7456),
#     (-45.8876, -21.7512),
#     (-45.8967, -21.7512),
#     (-45.8967, -21.7423),
#     (-45.8923, -21.7342)
# ])
# talhao1 = Field(
#     id=uuid4(),
#     estate_id=estate.id,
#     creator_id=user.id,
#     slug='cafe-mococa',
#     label='Café - Mococa (Mundo Novo)',
#     boundary=from_shape(talhao1_polygon, srid=4326),
#     boundary_source='GPS',
#     soil_type='Latossolo Vermelho-Amarelo distrófico',
#     slope_class='ondulado (8-20%)',
#     drainage_class='bem drenado',
#     created_at=datetime.now(),
#     updated_at=datetime.now()
# )
# db.add(talhao1)

# # Talhão 2: Café - 38 hectares (Caturaí, maior altitude)
# talhao2_polygon = Polygon([
#     (-45.8876, -21.7512),
#     (-45.8745, -21.7512),
#     (-45.8656, -21.7654),
#     (-45.8656, -21.7789),
#     (-45.8776, -21.7845),
#     (-45.8876, -21.7741),
#     (-45.8876, -21.7512)
# ])
# talhao2 = Field(
#     id=uuid4(),
#     estate_id=estate.id,
#     creator_id=user.id,
#     slug='cafe-alto',
#     label='Café - Caturaí (Alto da Serra)',
#     boundary=from_shape(talhao2_polygon, srid=4326),
#     boundary_source='GPS',
#     soil_type='Cambissolo Háplico',
#     slope_class='forte ondulado (20-45%)',
#     drainage_class='moderadamente drenado',
#     created_at=datetime.now(),
#     updated_at=datetime.now()
# )
# db.add(talhao2)

# # Talhão 3: Pastagem - 52 hectares (Fundo do vale, próximo ao córrego)
# talhao3_polygon = Polygon([
#     (-45.8842, -21.8015),
#     (-45.8623, -21.8015),
#     (-45.8523, -21.7895),
#     (-45.8478, -21.7741),
#     (-45.8556, -21.7684),
#     (-45.8656, -21.7789),
#     (-45.8776, -21.7845),
#     (-45.8842, -21.8015)
# ])
# talhao3 = Field(
#     id=uuid4(),
#     estate_id=estate.id,
#     creator_id=user.id,
#     slug='pastagem-fundo',
#     label='Pastagem - Fundo do Vale',
#     boundary=from_shape(talhao3_polygon, srid=4326),
#     boundary_source='GPS',
#     soil_type='Gleissolo Háplico',
#     slope_class='plano (0-3%)',
#     drainage_class='mal drenado (várzea)',
#     created_at=datetime.now(),
#     updated_at=datetime.now()
# )
# db.add(talhao3)

# # Talhão 4: Reserva Legal - 25 hectares (APP + Reserva)
# talhao4_polygon = Polygon([
#     (-45.8978, -21.7956),
#     (-45.8978, -21.7741),
#     (-45.9021, -21.7654),
#     (-45.9034, -21.7756),
#     (-45.9012, -21.7882),
#     (-45.8978, -21.7956)
# ])
# talhao4 = Field(
#     id=uuid4(),
#     estate_id=estate.id,
#     creator_id=user.id,
#     slug='reserva-mata',
#     label='Reserva Legal - Mata Atlântica',
#     boundary=from_shape(talhao4_polygon, srid=4326),
#     boundary_source='GPS + Imagem satélite',
#     soil_type='Neossolo Litólico',
#     slope_class='montanhoso (>45%)',
#     created_at=datetime.now(),
#     updated_at=datetime.now()
# )
# """

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

# async def _check_field_within_estate(
#     self,
#     field_boundary: WKBElement,
#     estate_id: UUID,
# ) -> None:
#     estate = await self.estate_repo.get_one(estate_id)
#     if estate.boundary is None:
#         return  # estate sem boundary — sem validação possível
#     estate_shape = wkb_to_shape(estate.boundary)
#     field_shape = wkb_to_shape(field_boundary)
#     if not estate_shape.contains(field_shape):
#         raise AgroAPIError(code='field.outside_estate_boundary')
