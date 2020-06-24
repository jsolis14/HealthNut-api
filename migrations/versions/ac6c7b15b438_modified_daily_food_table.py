"""modified daily food table

Revision ID: ac6c7b15b438
Revises: ac71c50d4925
Create Date: 2020-06-23 17:19:38.292828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac6c7b15b438'
down_revision = 'ac71c50d4925'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('daily_foods', sa.Column('breakfast_foods', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('breakfast_meals', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('dinner_foods', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('dinner_meals', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('lunch_foods', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('lunch_meals', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('snack_foods', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('daily_foods', sa.Column('snack_meals', sa.ARRAY(sa.Integer()), nullable=True))
    op.drop_constraint('daily_foods_food_id_fkey', 'daily_foods', type_='foreignkey')
    op.drop_constraint('daily_foods_meal_id_fkey', 'daily_foods', type_='foreignkey')
    op.drop_column('daily_foods', 'food_id')
    op.drop_column('daily_foods', 'meal_id')
    op.drop_column('daily_foods', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('daily_foods', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('daily_foods', sa.Column('meal_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('daily_foods', sa.Column('food_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('daily_foods_meal_id_fkey', 'daily_foods', 'meal', ['meal_id'], ['id'])
    op.create_foreign_key('daily_foods_food_id_fkey', 'daily_foods', 'foods', ['food_id'], ['id'])
    op.drop_column('daily_foods', 'snack_meals')
    op.drop_column('daily_foods', 'snack_foods')
    op.drop_column('daily_foods', 'lunch_meals')
    op.drop_column('daily_foods', 'lunch_foods')
    op.drop_column('daily_foods', 'dinner_meals')
    op.drop_column('daily_foods', 'dinner_foods')
    op.drop_column('daily_foods', 'breakfast_meals')
    op.drop_column('daily_foods', 'breakfast_foods')
    # ### end Alembic commands ###
