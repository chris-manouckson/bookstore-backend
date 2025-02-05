"""empty message

Revision ID: 72d0b38dd961
Revises: ee6447d35182
Create Date: 2020-07-07 01:05:59.293949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d0b38dd961'
down_revision = 'ee6447d35182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_roles', ['title'])
    op.create_unique_constraint(None, 'users', ['password'])
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'user_roles', type_='unique')
    # ### end Alembic commands ###
