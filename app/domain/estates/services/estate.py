from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.models.account import Account
from app.domain.estates.enums import EstateStatus
from app.domain.estates.models.estate import Estate
from app.domain.estates.schemas.estate import EstateCreate, EstateUpdate
from app.shared.authorization import require_permission
from app.shared.crud import CRUDBase
from app.shared.enums import Action, Resource
from app.shared.exceptions import (
    AgroAPIError,
    QuotaExceededError,
)
from app.shared.geometry import wkt_to_wkb
from app.shared.quota import QuotaService
from app.shared.service import BaseService

if TYPE_CHECKING:
    from app.domain.accounts.models.user import User


class EstateService(BaseService[Estate, EstateCreate, EstateUpdate]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Estate, session)
        self.account_repo = CRUDBase[Account](Account, session)

    @require_permission(Resource.ESTATE, Action.CREATE)
    async def create(self, data: EstateCreate, current_user: User) -> Estate:
        # quota check
        estate_count = await self._count_estates(current_user.account_id)
        if not QuotaService.check(
            current_user.account.plan, 'estates', estate_count
        ):
            raise QuotaExceededError('estate')

        # boundary overlap check
        boundary_wkb = None
        if data.boundary_wkt:
            boundary_wkb = wkt_to_wkb(data.boundary_wkt)
            await self._check_boundary_overlap(boundary_wkb)

        entrance_point_wkb = None
        if data.entrance_point_wkt:
            entrance_point_wkb = wkt_to_wkb(data.entrance_point_wkt)

        estate = Estate(
            account_id=current_user.account_id,
            label=data.label,
            slug=data.slug,
            description=data.description,
            timezone=data.timezone,
            zone=data.zone.value,
            usage=data.usage.value if data.usage else None,
            ownership_type=data.ownership_type.value,
            opened_at=data.opened_at,
            declared_area_m2=data.declared_area_m2,
            boundary=boundary_wkb,
            entrance_point=entrance_point_wkb,
            boundary_source=data.boundary_source.value
            if data.boundary_source
            else None,
            status=EstateStatus.PENDING.value,
        )

        return await self.repo.save(estate)

    async def _count_estates(self, account_id: UUID) -> int:
        result = await self.session.scalar(
            select(func.count()).where(
                Estate.account_id == account_id,
                Estate.archived_at.is_(None),
            )
        )
        return result or 0

    async def _check_boundary_overlap(
        self,
        boundary_wkb,
        exclude_id: UUID | None = None,
    ) -> None:
        stmt = select(Estate).where(
            Estate.boundary.isnot(None),
            func.ST_Overlaps(Estate.boundary, boundary_wkb),
        )
        if exclude_id:
            stmt = stmt.where(Estate.id != exclude_id)
        existing = await self.session.scalar(stmt)
        if existing:
            raise AgroAPIError(code='estate.boundary_overlap')
