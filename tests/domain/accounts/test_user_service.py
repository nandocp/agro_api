from uuid import uuid4

import pytest

from app.domain.accounts.models import PLAN_QUOTAS
from app.domain.accounts.services import UserService
from app.shared.exceptions import NotFoundError, QuotaExceededError
from tests.factories.accounts import UserFactory


@pytest.mark.asyncio
async def test_show_non_existing_user(session, superuser):
    with pytest.raises(NotFoundError) as exc:
        await UserService(session).show(uuid4(), current_user=superuser)

    assert exc.value.code == 'not_found.user'


@pytest.mark.asyncio
async def test_create_user_with_non_existing_account(session, superuser):
    with pytest.raises(NotFoundError) as exc:
        await UserService(session).create({}, uuid4(), current_user=superuser)

    assert exc.value.code == 'not_found.account'


@pytest.mark.asyncio
async def test_create_user_exceeding_account_quota(
    session, account, superuser
):
    quota = PLAN_QUOTAS[account.plan].max_users + 1
    id = account.id

    for i in range(quota):
        await UserFactory.create(session, account_id=id)

    with pytest.raises(QuotaExceededError) as exc:
        await UserService(session).create({}, id, current_user=superuser)

    assert exc.value.code == 'quota.account.users_limit_reached'
