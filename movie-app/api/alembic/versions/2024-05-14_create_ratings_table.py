"""create ratings table

Revision ID: 3e86ae792d12
Revises: d076915eb12e
Create Date: 2024-05-14 03:02:41.952204

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e86ae792d12"
down_revision: Union[str, None] = "d076915eb12e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rating",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("rater_id", sa.Integer, nullable=False),
        sa.Column("movie_rated_id", sa.Integer, nullable=False),
        sa.Column("rating", sa.Float, nullable=False, default=0),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(
            ["rater_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["movie_rated_id"],
            ["movie.id"],
        ),
    )


def downgrade() -> None:
    op.drop_table("rating")
