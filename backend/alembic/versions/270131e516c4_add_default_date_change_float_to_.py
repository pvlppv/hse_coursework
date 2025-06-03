"""add default date, change float to decimal, add id autoincrement

Revision ID: 270131e516c4
Revises: 40a7518a2179
Create Date: 2024-11-21 21:08:41.927407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '270131e516c4'
down_revision: Union[str, None] = '40a7518a2179'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Set server_default for TIMESTAMP columns
    op.alter_column('posts', 'date', server_default=sa.text('now()'))
    op.alter_column('locations', 'date', server_default=sa.text('now()'))
    op.alter_column('health', 'date', server_default=sa.text('now()'))
    op.alter_column('activities', 'date', server_default=sa.text('now()'))
    op.alter_column('projects', 'date', server_default=sa.text('now()'))
    op.alter_column('users', 'date', server_default=sa.text('now()'))

    # Change Float to DECIMAL in health table
    op.alter_column('health', 'height',
                    type_=sa.DECIMAL(precision=5, scale=1),
                    existing_type=sa.Float)
    op.alter_column('health', 'weight',
                    type_=sa.DECIMAL(precision=5, scale=1),
                    existing_type=sa.Float)
    op.alter_column('health', 'heart_rate',
                    type_=sa.DECIMAL(precision=5, scale=1),
                    existing_type=sa.Float)
    op.alter_column('health', 'energy',
                    type_=sa.DECIMAL(precision=5, scale=1),
                    existing_type=sa.Float)
    op.alter_column('health', 'sleep',
                    type_=sa.DECIMAL(precision=5, scale=1),
                    existing_type=sa.Float)

    # Add autoincrement=True for id columns
    op.alter_column('posts', 'id', autoincrement=True, existing_type=sa.Integer)
    op.alter_column('locations', 'id', autoincrement=True, existing_type=sa.Integer)
    op.alter_column('health', 'id', autoincrement=True, existing_type=sa.Integer)
    op.alter_column('activities', 'id', autoincrement=True, existing_type=sa.Integer)
    op.alter_column('projects', 'id', autoincrement=True, existing_type=sa.Integer)
    op.alter_column('users', 'id', autoincrement=True, existing_type=sa.Integer)


def downgrade() -> None:
    # Remove server_default for TIMESTAMP columns
    op.alter_column('posts', 'date', server_default=None)
    op.alter_column('locations', 'date', server_default=None)
    op.alter_column('health', 'date', server_default=None)
    op.alter_column('activities', 'date', server_default=None)
    op.alter_column('projects', 'date', server_default=None)
    op.alter_column('users', 'date', server_default=None)

    # Change DECIMAL back to Float in health table
    op.alter_column('health', 'height',
                    type_=sa.Float,
                    existing_type=sa.DECIMAL(precision=5, scale=1))
    op.alter_column('health', 'weight',
                    type_=sa.Float,
                    existing_type=sa.DECIMAL(precision=5, scale=1))
    op.alter_column('health', 'heart_rate',
                    type_=sa.Float,
                    existing_type=sa.DECIMAL(precision=5, scale=1))
    op.alter_column('health', 'energy',
                    type_=sa.Float,
                    existing_type=sa.DECIMAL(precision=5, scale=1))
    op.alter_column('health', 'sleep',
                    type_=sa.Float,
                    existing_type=sa.DECIMAL(precision=5, scale=1))

    # Remove autoincrement=True for id columns
    op.alter_column('posts', 'id', autoincrement=None, existing_type=sa.Integer)
    op.alter_column('locations', 'id', autoincrement=None, existing_type=sa.Integer)
    op.alter_column('health', 'id', autoincrement=None, existing_type=sa.Integer)
    op.alter_column('activities', 'id', autoincrement=None, existing_type=sa.Integer)
    op.alter_column('projects', 'id', autoincrement=None, existing_type=sa.Integer)
    op.alter_column('users', 'id', autoincrement=None, existing_type=sa.Integer)
