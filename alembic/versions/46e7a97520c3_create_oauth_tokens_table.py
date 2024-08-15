"""create oauth tokens table

Revision ID: 46e7a97520c3
Revises: 2237b37e721f
Create Date: 2023-11-03 20:49:42.873114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "46e7a97520c3"
down_revision: Union[str, None] = "2237b37e721f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_oauth_tokens",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("revoked", sa.Boolean(), default=False),
    )


def downgrade() -> None:
    op.drop_table("user_oauth_tokens")
