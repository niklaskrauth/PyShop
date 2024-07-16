"""create account table

Revision ID: 8614ffc638fb
Revises:
Create Date: 2024-07-11 13:47:59.988914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8614ffc638fb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "articles2",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("imageUrl", sa.VARCHAR(255), nullable=True),
        sa.Column("first_name", sa.VARCHAR(255)),
        sa.Column("last_name", sa.VARCHAR(255)),
        sa.Column("price", sa.Float),
    )


def downgrade():
    pass
