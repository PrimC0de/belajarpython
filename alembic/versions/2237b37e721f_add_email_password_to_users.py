"""add email password to users

Revision ID: 2237b37e721f
Revises: 1329b225f9c5
Create Date: 2023-11-03 20:47:48.036924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2237b37e721f'
down_revision: Union[str, None] = '1329b225f9c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'email')
    op.drop_column('users', 'password')
