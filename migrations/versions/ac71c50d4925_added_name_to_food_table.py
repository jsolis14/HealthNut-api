"""added name to food table

Revision ID: ac71c50d4925
Revises: 9227bc6cf3fc
Create Date: 2020-06-22 10:15:04.027712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac71c50d4925'
down_revision = '9227bc6cf3fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foods', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('foods', 'name')
    # ### end Alembic commands ###
