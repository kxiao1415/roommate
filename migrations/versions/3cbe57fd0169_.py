"""empty message

Revision ID: 3cbe57fd0169
Revises: 5fb91991ef84
Create Date: 2018-02-03 19:50:15.697075

"""

# revision identifiers, used by Alembic.
revision = '3cbe57fd0169'
down_revision = '5fb91991ef84'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('last_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
