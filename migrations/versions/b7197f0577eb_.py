"""empty message

Revision ID: b7197f0577eb
Revises: 80f61f0979a0
Create Date: 2020-02-16 18:23:09.989806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7197f0577eb'
down_revision = '80f61f0979a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game4',
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
    sa.Column('b1', sa.Boolean(), nullable=True),
    sa.Column('b2', sa.Boolean(), nullable=True),
    sa.Column('b3', sa.Boolean(), nullable=True),
    sa.Column('b4', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game4_date'), 'game4', ['date'], unique=True)
    op.create_table('game5',
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
    sa.Column('b1', sa.Boolean(), nullable=True),
    sa.Column('b2', sa.Boolean(), nullable=True),
    sa.Column('b3', sa.Boolean(), nullable=True),
    sa.Column('b4', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game5_date'), 'game5', ['date'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game5_date'), table_name='game5')
    op.drop_table('game5')
    op.drop_index(op.f('ix_game4_date'), table_name='game4')
    op.drop_table('game4')
    # ### end Alembic commands ###
