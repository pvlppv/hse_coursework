"""sessions is_active

Revision ID: 75bb6f58ecd6
Revises: a1c84039dbcd
Create Date: 2025-02-02 20:46:43.637338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75bb6f58ecd6'
down_revision: Union[str, None] = 'a1c84039dbcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sessions', sa.Column('is_active', sa.Boolean(), default=True))


def downgrade() -> None:
    op.drop_column('sessions', 'is_active')