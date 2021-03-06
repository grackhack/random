"""empty message

Revision ID: 038b73675e66
Revises: beb249720b87
Create Date: 2020-01-15 23:27:09.615826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038b73675e66'
down_revision = 'beb249720b87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('play', sa.Column('game_koef', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('play', 'game_koef')
    # ### end Alembic commands ###
