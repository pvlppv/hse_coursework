"""add sessions table

Revision ID: fdab50e28bd1
Revises: 4ed8806efbb1
Create Date: 2025-02-02 19:52:53.028877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'fdab50e28bd1'
down_revision: Union[str, None] = '4ed8806efbb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('end_time', sa.TIMESTAMP(timezone=True)),
        sa.Column('data_collection_methods', JSONB, nullable=False),
        sa.Column('visualization_preferences', JSONB, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_paused', sa.Boolean(), default=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop sessions table
    op.drop_table('sessions')