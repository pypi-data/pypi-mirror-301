"""Add indexes on history2

Revision ID: 6b30d917f125
Revises: f953dc7ec5a5
Create Date: 2024-10-05 17:13:00.623878+00:00

"""
# pylint: disable=no-member, invalid-name, missing-function-docstring, unused-import, no-name-in-module

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b30d917f125'
down_revision = 'f953dc7ec5a5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_history_user'), ['user'], unique=False)


def downgrade():
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_history_user'))
