"""create users table

Revision ID: 1329b225f9c5
Revises: 
Create Date: 2023-11-02 21:46:14.580458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1329b225f9c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.VARCHAR),
        sa.Column('active', sa.BOOLEAN, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('users')
