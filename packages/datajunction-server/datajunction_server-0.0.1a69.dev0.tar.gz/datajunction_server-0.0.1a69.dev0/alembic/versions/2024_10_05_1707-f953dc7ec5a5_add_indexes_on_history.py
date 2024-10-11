"""Add indexes on history

Revision ID: f953dc7ec5a5
Revises: f3c9b40deb6f
Create Date: 2024-10-05 17:07:17.320467+00:00

"""
# pylint: disable=no-member, invalid-name, missing-function-docstring, unused-import, no-name-in-module

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f953dc7ec5a5'
down_revision = 'f3c9b40deb6f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_history_entity_name'), ['entity_name'], unique=False)


def downgrade():
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_history_entity_name'))
