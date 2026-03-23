import pytest

from tests.factories.journal_entry import JournalEntryFactory


@pytest.mark.asyncio
async def test_journal_entry_repr_(session, user, estate):
    entry = await JournalEntryFactory.create(
        session,
        author_id=user.id,
        entity_type=estate.__class__.__name__,
        entity_id=estate.id,
    )

    tester = [
        f'id={entry.id}',
        f'entity={entry.entity_type}',
        f'title={entry.title[:19].strip()}',
        f'date={entry.logged_at.date()}',
    ]
    assert str(entry) == f'JournalEntry({", ".join(tester)})'
    assert entry.entity_type == 'Estate'
