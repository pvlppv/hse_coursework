"""add_goals_to_sessions

Revision ID: 67c76c70fd5c
Revises: 75bb6f58ecd6
Create Date: 2025-06-06 11:15:55.023212

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "67c76c70fd5c"
down_revision: Union[str, None] = "75bb6f58ecd6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add goal_type column
    op.add_column("sessions", sa.Column("goal_type", sa.String(), nullable=True))

    # Add metric column as JSONB
    op.add_column("sessions", sa.Column("metric", JSONB, nullable=True))


def downgrade() -> None:
    # Remove metric column
    op.drop_column("sessions", "metric")

    # Remove goal_type column
    op.drop_column("sessions", "goal_type")
