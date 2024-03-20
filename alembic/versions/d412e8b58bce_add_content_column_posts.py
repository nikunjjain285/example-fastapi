"""add_content_column_posts

Revision ID: d412e8b58bce
Revises: 8ed77f11718a
Create Date: 2024-03-20 12:25:24.961590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd412e8b58bce'
down_revision: Union[str, None] = '8ed77f11718a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
