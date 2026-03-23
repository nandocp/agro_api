from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from app.domain.accounts.models.user import User
from app.shared.authorization import AuthorizationService, require_permission
from app.shared.enums import Action, Resource
from app.shared.exceptions import UnauthorizedError
from tests.factories.accounts import UserFactory


def make_user_with_permission(resource: Resource, action: Action) -> User:
    permission = MagicMock()
    permission.resource = resource.value
    permission.action = action.value

    role = MagicMock()
    role.permissions = [permission]

    user = MagicMock(spec=User)
    user.roles = [role]
    user.deactivated_at = None
    return user


def make_user_without_permissions() -> User:
    user = MagicMock(spec=User)
    user.roles = []
    user.deactivated_at = None
    return user


# stub service para testar o decorator
class StubService:
    @require_permission(Resource.ESTATE, Action.CREATE)
    async def create(self, data: str, current_user: User) -> str:  # noqa: PLR6301
        return 'created'


@pytest.mark.asyncio
async def test_require_permission_with_kwarg():
    """current_user passed as keyword argument."""
    service = StubService()
    user = make_user_with_permission(Resource.ESTATE, Action.CREATE)
    result = await service.create('data', current_user=user)
    assert result == 'created'


@pytest.mark.asyncio
async def test_require_permission_with_positional_arg():
    """current_user passed as positional argument — fallback path."""
    service = StubService()
    user = make_user_with_permission(Resource.ESTATE, Action.CREATE)
    result = await service.create('data', user)  # posicional
    assert result == 'created'


@pytest.mark.asyncio
async def test_require_permission_no_current_user_raises():
    """No current_user in args or kwargs."""
    service = StubService()
    with pytest.raises(UnauthorizedError):
        await service.create('data')  # sem current_user


@pytest.mark.asyncio
async def test_require_permission_unauthorized_raises():
    """User without required permission."""
    service = StubService()
    user = make_user_without_permissions()
    with pytest.raises(UnauthorizedError):
        await service.create('data', current_user=user)


@pytest.mark.asyncio
async def test_has_permission_for_deactivated_user():
    user = await UserFactory.build()
    user.deactivated_at = datetime.now() - timedelta(seconds=1)

    assert not AuthorizationService.has_permission(
        user, Resource.ACCOUNT, Action.APPROVE
    )
