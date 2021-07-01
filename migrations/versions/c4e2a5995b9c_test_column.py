"""test column

Revision ID: c4e2a5995b9c
Revises: 49f6274246c3
Create Date: 2021-06-21 14:00:28.816667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e2a5995b9c'
down_revision = '49f6274246c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authors', sa.Column('test_column', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authors', 'test_column')
    # ### end Alembic commands ###
