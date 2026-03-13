import pytest

from tests.factories.accounts import AccountFactory, UserFactory


@pytest.mark.asyncio
async def test_user_repr_(session):
    account = await AccountFactory.create(session)
    user = await UserFactory.create(session, account_id=account.id)
    repr_attrs = [f'id={user.id}', f'name={user.name}', f'email={user.email}']
    assert str(user) == f'User({(", ".join(repr_attrs))})'
