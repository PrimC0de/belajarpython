"""Create books table

Revision ID: 7fd011c516f1
Revises: 738f21045eb0
Create Date: 2024-08-15 19:05:50.751371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fd011c516f1'
down_revision: Union[str, None] = '738f21045eb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, index=True),
        sa.Column('isbn', sa.String, unique=True),
        sa.Column('author', sa.String)
    )


def downgrade() -> None:
    op.drop_table('books')
