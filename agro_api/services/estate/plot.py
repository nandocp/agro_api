from datetime import datetime
from typing import List, Optional

from shapely.validation import explain_validity

from agro_api.entities.estate import Plot
from agro_api.repositories.estate import EstateRepository
from agro_api.services.base import BaseService
from config.error_responses import unauthorized, unprocessable
from config.geometry import create_polygon_geometry, shape_to_wkb, wkb_to_shape


def verify_limits(estate, plot):
    estate_limits = wkb_to_shape(estate.limits)
    plot_limits = wkb_to_shape(plot.limits)

    limits_present = estate_limits and plot_limits
    plot_inside_estate = estate_limits.contains(plot_limits)

    if limits_present and not plot_inside_estate:
        unprocessable('Plot not inside Estate limits')

    return True


class PlotService(BaseService):
    def __init__(self, session=None, user=None):
        super().__init__(Plot, session, user)

    async def create(self, create_params, estate_id) -> Plot:
        # 0. Verify if estate_id's are matching
        if not str(create_params.estate_id) == estate_id:
            unauthorized()

        find_params = {'id': estate_id, 'user_id': self.user.id}
        estate = await EstateRepository(self.session).find_by(find_params)

        # 1. A User can only create Plots on Estates owned by them
        if not estate:
            unauthorized()

        # 2. A Plot must not be placed outside the limits of a Estate
        verify_limits(estate, create_params)

        active_plots = await self.repository.get_active(estate_id)
        limits = create_params.limits
        breakpoint()
        if limits:
            limits = create_polygon_geometry(limits)

            # 3. A new Plot cannot overlap other active Plots
            if any(limits.intersect(plot.limits) for plot in active_plots):
                unprocessable('Plot is overlaping')
        elif estate.limits and len(active_plots) == 0:
            # 4. If params has no limits AND estate has no active Plot
            limits = wkb_to_shape(estate.limits)

        if limits and not limits.is_valid:
            unprocessable(explain_validity(limits))

        create_params.limits = shape_to_wkb(limits)

        if not create_params.slug:
            now = datetime.now()
            now.strftime('')
            create_params.slug = f'plot#{now.strftime("%Y%m%d%H%M%S")}'

        return await self.repository.create(create_params, estate)

    def get_one(self, id: int) -> Optional[Plot]:
        pass  # pragma: no cover

    def get_many(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[Plot]:
        pass  # pragma: no cover

    def update(self, *, obj_id: str, obj_in) -> Plot:
        pass  # pragma: no cover

    def remove(self, *, id: int) -> None:
        pass  # pragma: no cover
