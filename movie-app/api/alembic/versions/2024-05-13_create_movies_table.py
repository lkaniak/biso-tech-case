"""create movies table

Revision ID: d076915eb12e
Revises: 26a39ec9f9cc
Create Date: 2024-05-13 19:39:56.787415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d076915eb12e"
down_revision: Union[str, None] = "26a39ec9f9cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movie",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(1024), nullable=False),
        sa.Column("genres", sa.String(512), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("movie")
