from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.enums import AccountPlan
from app.domain.accounts.models import Account, Role, User, user_roles
from app.shared.security import hash_password
from config.settings import settings


async def seed(session: AsyncSession) -> None:
    existing = await session.scalar(
        select(User).where(User.email == settings.SUPERADMIN_EMAIL)
    )
    if existing:
        return

    account = Account(
        name='Institutional',
        document='00000000000000',
        plan=AccountPlan.ENTERPRISE,
    )
    session.add(account)
    await session.flush()

    email = settings.SUPERADMIN_EMAIL
    password = settings.SUPERADMIN_PASSWORD
    if settings.ENVIRONMENT == 'production' and (
        email == 'user@system.br' or password == 'password'
    ):
        raise RuntimeError(
            f'Forbidden {settings.ENVIRONMENT} superadmin credentials'
        )
    user = User(
        name='Super Admin',
        email=email,
        password=hash_password(password),
        account_id=account.id,
    )
    session.add(user)
    await session.flush()

    superuser_role = await session.scalar(
        select(Role).where(Role.name == 'superuser')
    )
    await session.execute(
        insert(user_roles)
        .values(user_id=user.id, role_id=superuser_role.id)
        .on_conflict_do_nothing()
    )

    await session.commit()
