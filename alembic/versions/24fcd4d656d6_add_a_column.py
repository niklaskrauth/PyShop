"""Add a column

Revision ID: 24fcd4d656d6
Revises: 8614ffc638fb
Create Date: 2024-07-11 14:10:53.078545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '24fcd4d656d6'
down_revision: Union[str, None] = '8614ffc638fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('articles2', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('articles2', 'last_transaction_date')
