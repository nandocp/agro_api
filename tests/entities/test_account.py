import pytest


@pytest.mark.asyncio
async def test_account_repr_(account):
    assert str(account) == f'Account(id={account.id}, name={account.name})'
