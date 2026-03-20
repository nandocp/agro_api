from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.models.rbac import (
    Permission,
    Role,
    role_permissions,
)
from app.shared.enums import Action, Resource

PERMISSIONS_MATRIX = {
    'superuser': [
        (Resource.ACCOUNT, Action.CREATE),
        (Resource.ACCOUNT, Action.UPDATE),
        (Resource.ACCOUNT, Action.ARCHIVE),
        (Resource.USER, Action.CREATE),
        (Resource.USER, Action.UPDATE),
        (Resource.USER, Action.DEACTIVATE),
        (Resource.ESTATE, Action.APPROVE),
    ],
    'admin': [
        (Resource.ACCOUNT, Action.UPDATE),
        (Resource.USER, Action.CREATE),
        (Resource.USER, Action.UPDATE),
        (Resource.USER, Action.DEACTIVATE),
        (Resource.ESTATE, Action.CREATE),
        (Resource.ESTATE, Action.UPDATE),
        (Resource.ESTATE, Action.ARCHIVE),
        (Resource.ESTATE, Action.EXPORT),
        (Resource.FIELD, Action.CREATE),
        (Resource.FIELD, Action.UPDATE),
        (Resource.FIELD, Action.ARCHIVE),
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.CANCEL),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.CREATE),
        (Resource.TASK, Action.UPDATE),
        (Resource.TASK, Action.ASSIGN),
        (Resource.TASK, Action.CANCEL),
        (Resource.TASK, Action.EXPORT),
    ],
    'manager': [
        (Resource.ESTATE, Action.UPDATE),
        (Resource.ESTATE, Action.EXPORT),
        (Resource.FIELD, Action.CREATE),
        (Resource.FIELD, Action.UPDATE),
        (Resource.FIELD, Action.ARCHIVE),
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.CANCEL),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.CREATE),
        (Resource.TASK, Action.UPDATE),
        (Resource.TASK, Action.ASSIGN),
        (Resource.TASK, Action.CANCEL),
        (Resource.TASK, Action.EXPORT),
    ],
    'agronomist': [
        (Resource.ACTIVITY, Action.CREATE),
        (Resource.ACTIVITY, Action.UPDATE),
        (Resource.ACTIVITY, Action.APPROVE),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.ESTATE, Action.EXPORT),
    ],
    'worker': [
        (Resource.ACTIVITY, Action.EXECUTE),
        (Resource.ACTIVITY, Action.EXPORT),
        (Resource.TASK, Action.EXECUTE),
        (Resource.TASK, Action.EXPORT),
    ],
}


async def seed_permissions(session: AsyncSession) -> dict[tuple, Permission]:
    all_pairs = {
        (resource, action)
        for permissions in PERMISSIONS_MATRIX.values()
        for resource, action in permissions
    }

    for resource, action in all_pairs:
        await session.execute(
            insert(Permission)
            .values(resource=resource.value, action=action.value)
            .on_conflict_do_nothing(constraint='uq_permission_resource_action')
        )
    await session.flush()

    result = await session.scalars(select(Permission))
    return {(p.resource, p.action): p for p in result.all()}


async def seed_roles(
    session: AsyncSession, permission_map: dict[tuple, Permission]
) -> None:
    for role_name, permissions in PERMISSIONS_MATRIX.items():
        await session.execute(
            insert(Role).values(name=role_name).on_conflict_do_nothing()
        )
        await session.flush()

        role = await session.scalar(select(Role).where(Role.name == role_name))

        for resource, action in permissions:
            permission = permission_map[(resource.value, action.value)]
            await session.execute(
                insert(role_permissions)
                .values(role_id=role.id, permission_id=permission.id)
                .on_conflict_do_nothing(constraint='uq_role_name')
            )

    await session.flush()


async def seed(session: AsyncSession) -> None:
    permission_map = await seed_permissions(session)
    await seed_roles(session, permission_map)
