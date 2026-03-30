from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.models import Role, user_roles
from app.domain.accounts.schemas import UserRoleCreate
from app.shared.exceptions import NotFoundError


class RbacRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def assign_role(self, params: UserRoleCreate) -> None:
        role = await self.session.scalar(
            select(Role).where(Role.name == params.role)
        )

        await self.session.execute(
            insert(user_roles)
            .values(user_id=params.user_id, role_id=role.id)
            .on_conflict_do_nothing()
        )

    async def revoke_role(self, params: UserRoleCreate) -> None:
        role = await self.session.scalar(
            select(Role).where(Role.name == params.role)
        )

        if not role:
            raise NotFoundError('role')

        await self.session.execute(
            delete(user_roles).where(
                user_roles.c.user_id == params.user_id,
                user_roles.c.role_id == role.id,
            )
        )
