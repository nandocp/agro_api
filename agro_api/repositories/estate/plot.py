from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from agro_api.entities.estate import Plot
from agro_api.repositories.base import BaseRepository
from config.http_misc import unprocessable


class PlotRepository(BaseRepository):
    async def find_by_id(self, id: str) -> Plot:
        return await self.session.scalar(select(Plot).where(Plot.id == id))

    async def get_active(self, estate_id=None):
        stmt = select(Plot).where(Plot.status == 'active')
        if estate_id:
            stmt = stmt.where(Plot.estate_id == estate_id)

        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, params_schema, estate) -> Plot:
        new_plot = Plot(
            estate_id=params_schema.estate_id,
            slug=params_schema.slug,
            label=params_schema.label,
            land_use=params_schema.land_use,
            status=params_schema.status,
        )

        if params_schema.limits:
            new_plot.limits = params_schema.limits

        self.session.add(new_plot)

        try:
            await self.session.commit()
            await self.session.refresh(new_plot)

            return new_plot
        except IntegrityError:
            unprocessable('Plot slug already exists')
