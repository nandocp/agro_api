from agro_api.entities.estate import Plot
from agro_api.repositories.base import BaseRepository
from agro_api.schemas.estate import PlotCreate, PlotUpdate


class PlotRepository(BaseRepository[Plot, PlotCreate, PlotUpdate]):
    pass
