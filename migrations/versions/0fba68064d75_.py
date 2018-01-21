"""empty message

Revision ID: 0fba68064d75
Revises: 43fa806a4f8b
Create Date: 2018-01-21 05:29:32.634140

"""

# revision identifiers, used by Alembic.
revision = '0fba68064d75'
down_revision = '43fa806a4f8b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'preference', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'preference', type_='unique')
    # ### end Alembic commands ###