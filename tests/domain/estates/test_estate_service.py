import pytest

from app.domain.accounts.enums import AccountPlan
from app.shared.exceptions import (
    AgroAPIError,
    QuotaExceededError,
    UnauthorizedError,
)
from tests.domain.estates.conftest import OVERLAPPING_BOUNDARY_WKT
from tests.factories.accounts import AccountFactory
from tests.factories.estates import EstateFactory


@pytest.mark.asyncio
async def test_admin_user_create_estate(
    estate_service, estate_create, admin_user
):
    estate = await estate_service.create(
        estate_create, current_user=admin_user
    )

    assert estate.id is not None
    assert estate.account_id == admin_user.account_id
    assert estate.slug == estate_create.slug
    assert estate.label == estate_create.label


@pytest.mark.asyncio
async def test_user_without_role_cannot_create_estate(
    estate_service, estate_create, user
):
    with pytest.raises(UnauthorizedError) as exc:
        await estate_service.create(estate_create, current_user=user)

    assert exc.value.code == 'auth.unauthorized'


@pytest.mark.asyncio
async def test_create_estate_exceeds_free_plan_quota(
    estate_service, estate_create, admin_user, session
):
    await estate_service.create(estate_create, current_user=admin_user)
    await session.flush()

    with pytest.raises(QuotaExceededError) as exc:
        await estate_service.create(estate_create, current_user=admin_user)

    assert exc.value.code == 'quota.estate_limit_reached'


async def test_create_estate_boundary_overlap_for_same_account(
    estate_service,
    estate_create,
    admin_user,
    session,
    account,
):
    account.plan = AccountPlan.PRO
    session.add(account)
    await session.flush()
    await EstateFactory.create(session, account_id=account.id)

    estate_create.boundary_wkt = OVERLAPPING_BOUNDARY_WKT
    with pytest.raises(AgroAPIError) as exc:
        await estate_service.create(estate_create, current_user=admin_user)
    assert exc.value.code == 'estate.boundary_overlap'


async def test_create_estate_boundary_overlap_for_different_account(
    estate_service, estate_create, admin_user, session, account
):
    await EstateFactory.create(session, account_id=account.id)

    new_account = await AccountFactory.create(session)
    admin_user.account_id = new_account.id
    session.add(admin_user)
    await session.flush()

    estate_create.boundary_wkt = OVERLAPPING_BOUNDARY_WKT
    with pytest.raises(AgroAPIError) as exc:
        await estate_service.create(estate_create, current_user=admin_user)
    assert exc.value.code == 'estate.boundary_overlap'
