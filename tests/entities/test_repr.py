import pytest


@pytest.mark.asyncio
async def test_account(account):
    assert str(account) == f'Account(id={account.id}, name={account.name})'


@pytest.mark.asyncio
async def test_user(user):
    assert str(user) == f'User(id={user.id}, name={user.name})'


@pytest.mark.asyncio
async def test_estate(estate):
    repr_attrs = [
        f'id={estate.id}',
        f'slug={estate.slug}',
        f'created_at={estate.created_at}'
    ]
    assert str(estate) == f'Estate({(', '.join(repr_attrs))})'


@pytest.mark.asyncio
async def test_plot(plot):
    _repr = f'Plot(id={plot.id}, slug={plot.slug}, estate={plot.estate.slug})'
    assert str(plot) == _repr
