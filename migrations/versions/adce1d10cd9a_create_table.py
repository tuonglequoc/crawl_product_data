"""Create table

Revision ID: adce1d10cd9a
Revises: 
Create Date: 2021-06-04 00:35:08.399162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adce1d10cd9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('barcode', sa.BigInteger(), nullable=False),
    sa.Column('product_name', sa.Text(), nullable=True),
    sa.Column('category', sa.Text(), nullable=True),
    sa.Column('country_of_origin', sa.Text(), nullable=True),
    sa.Column('link', sa.Text(), nullable=True),
    sa.Column('thumbnail', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('remarks', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('barcode')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
