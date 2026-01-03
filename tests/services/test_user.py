from uuid import uuid4

import pytest

from agro_api.services.user import UserService


@pytest.mark.asyncio
async def test_get_one_user_with_mismatching_id(session, user, other_user):
    service = await UserService(session).get_one(
        user.id, other_user.jti
    )

    assert not service


@pytest.mark.asyncio
async def test_update_with_incorrect_id(session):
    service = await UserService(session).update(uuid4(), {})

    assert not service
