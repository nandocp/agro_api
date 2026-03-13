"""create postgis extension

Revision ID: c5dfc671ace3
Revises:
Create Date: 2026-03-12 22:29:56.802120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5dfc671ace3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP EXTENSION postgis CASCADE;')
