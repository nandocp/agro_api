import pytest

from tests.factories.accounts import AccountFactory


@pytest.mark.asyncio
async def test_account_repr_(session):
    account = await AccountFactory.create(session)
    assert str(account) == f'Account(id={account.id}, name={account.name})'
