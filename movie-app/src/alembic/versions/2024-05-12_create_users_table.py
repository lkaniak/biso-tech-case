"""create users table

Revision ID: 26a39ec9f9cc
Revises: 
Create Date: 2024-05-12 16:59:43.191111

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "26a39ec9f9cc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(150), nullable=False),
        sa.Column("full_name", sa.String(150), nullable=True),
        sa.Column("nickname", sa.String(150), nullable=False),
        sa.Column("hashed_password", sa.String(300), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("is_superuser", sa.Boolean, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
