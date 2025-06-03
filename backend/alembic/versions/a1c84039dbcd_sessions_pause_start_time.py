"""sessions pause_start_time

Revision ID: a1c84039dbcd
Revises: fdab50e28bd1
Create Date: 2025-02-02 20:33:37.561536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c84039dbcd'
down_revision: Union[str, None] = 'fdab50e28bd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sessions', sa.Column('pause_start_time', sa.TIMESTAMP(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('sessions', 'pause_start_time')