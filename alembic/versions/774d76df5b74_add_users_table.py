"""add_users_table

Revision ID: 774d76df5b74
Revises: d412e8b58bce
Create Date: 2024-03-20 16:10:43.352925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '774d76df5b74'
down_revision: Union[str, None] = 'd412e8b58bce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String(),nullable=False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()')),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
