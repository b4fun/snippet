"""add_quote_table

Revision ID: 2e507651d7bf
Revises:
Create Date: 2019-08-12 22:34:44.725138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e507651d7bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'quote',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('message', sa.Text, comment='the quote mesage')
    )


def downgrade():
    op.drop_table('quote')
