"""user  table

Revision ID: f97fe304c57a
Revises: a3b3d154fcf2
Create Date: 2019-12-22 22:50:23.266479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f97fe304c57a'
down_revision = 'a3b3d154fcf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('balance', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'balance')
    # ### end Alembic commands ###