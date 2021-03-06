"""revert to initial version

Revision ID: 49f6274246c3
Revises: 5246ecaf4f33
Create Date: 2021-06-21 13:57:26.725871

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '49f6274246c3'
down_revision = '5246ecaf4f33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('book')
    op.drop_table('author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('author_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('created', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='author_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='book_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='book_pkey')
    )
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###
