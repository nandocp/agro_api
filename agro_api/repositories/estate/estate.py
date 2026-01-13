from agro_api.entities.estate import Estate
from agro_api.repositories.base import BaseRepository
from agro_api.schemas.estate import EstateBase, EstateCreate


class EstateRepository(BaseRepository[Estate, EstateCreate, EstateBase]):
    pass
