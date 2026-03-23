from datetime import datetime

import factory

from app.shared.journal.entry import JournalEntry

from .async_factory import AsyncSQLAlchemyFactory

Faker = factory.Faker


class JournalEntryFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = JournalEntry

    logged_at = datetime.now()
    title = Faker('sentence')
    content = Faker('text')
