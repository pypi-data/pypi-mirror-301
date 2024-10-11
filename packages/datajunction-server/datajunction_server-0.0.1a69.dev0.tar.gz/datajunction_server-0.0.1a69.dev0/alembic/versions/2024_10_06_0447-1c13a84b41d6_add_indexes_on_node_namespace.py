"""Add indexes on node namespace

Revision ID: 1c13a84b41d6
Revises: 90d6250dc394
Create Date: 2024-10-06 04:47:18.214335+00:00

"""
# pylint: disable=no-member, invalid-name, missing-function-docstring, unused-import, no-name-in-module

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c13a84b41d6'
down_revision = '90d6250dc394'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('node', schema=None) as batch_op:
        batch_op.create_index('namespace_index', ['namespace'], unique=False, postgresql_using='btree', postgresql_ops={"identifier": "varchar_pattern_ops"},)


def downgrade():
    with op.batch_alter_table('node', schema=None) as batch_op:
        batch_op.drop_index('namespace_index', postgresql_using='text_pattern_ops')
