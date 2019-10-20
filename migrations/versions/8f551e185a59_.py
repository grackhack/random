"""empty message

Revision ID: 8f551e185a59
Revises: 23d7ec5d47cb
Create Date: 2019-10-20 11:57:47.453596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f551e185a59'
down_revision = '23d7ec5d47cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('de1', sa.Boolean(), nullable=True),
    sa.Column('de2', sa.Boolean(), nullable=True),
    sa.Column('de3', sa.Boolean(), nullable=True),
    sa.Column('de4', sa.Boolean(), nullable=True),
    sa.Column('de5', sa.Boolean(), nullable=True),
    sa.Column('de6', sa.Boolean(), nullable=True),
    sa.Column('de7', sa.Boolean(), nullable=True),
    sa.Column('de8', sa.Boolean(), nullable=True),
    sa.Column('de9', sa.Boolean(), nullable=True),
    sa.Column('de10', sa.Boolean(), nullable=True),
    sa.Column('de11', sa.Boolean(), nullable=True),
    sa.Column('de12', sa.Boolean(), nullable=True),
    sa.Column('de13', sa.Boolean(), nullable=True),
    sa.Column('de14', sa.Boolean(), nullable=True),
    sa.Column('de15', sa.Boolean(), nullable=True),
    sa.Column('de16', sa.Boolean(), nullable=True),
    sa.Column('de17', sa.Boolean(), nullable=True),
    sa.Column('de18', sa.Boolean(), nullable=True),
    sa.Column('de19', sa.Boolean(), nullable=True),
    sa.Column('de20', sa.Boolean(), nullable=True),
    sa.Column('de21', sa.Boolean(), nullable=True),
    sa.Column('de22', sa.Boolean(), nullable=True),
    sa.Column('de23', sa.Boolean(), nullable=True),
    sa.Column('de24', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_date'), 'game', ['date'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_date'), table_name='game')
    op.drop_table('game')
    # ### end Alembic commands ###
