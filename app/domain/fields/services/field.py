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
