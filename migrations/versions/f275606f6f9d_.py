"""empty message

Revision ID: f275606f6f9d
Revises: b8f5434a9892
Create Date: 2020-07-07 00:40:39.241182

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f275606f6f9d'
down_revision = 'b8f5434a9892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('price_ammount', sa.Float(), nullable=True))
    op.add_column('books', sa.Column('price_currency', sa.String(), nullable=True))
    op.drop_column('books', 'price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('price', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('books', 'price_currency')
    op.drop_column('books', 'price_ammount')
    # ### end Alembic commands ###
