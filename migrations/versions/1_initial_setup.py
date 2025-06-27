"""Initial setup

Revision ID: 1
Revises: 
Create Date: 2025-06-26 20:18:00.123456

"""
from alembic import op
import sqlalchemy as sa

revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('books',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('author', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('reviews',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=True),
                    sa.Column('content', sa.String(), nullable=True),
                    sa.Column('rating', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_reviews_book_id'), 'reviews', ['book_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_reviews_book_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_table('books')