"""empty message

Revision ID: 7b0fd250cd7a
Revises: f97fe304c57a
Create Date: 2020-01-14 22:38:10.604579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b0fd250cd7a'
down_revision = 'f97fe304c57a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game2',
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
    sa.Column('de25', sa.Boolean(), nullable=True),
    sa.Column('de26', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game2_date'), 'game2', ['date'], unique=True)
    op.create_table('game3',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('de0', sa.Boolean(), nullable=True),
    sa.Column('de1', sa.Boolean(), nullable=True),
    sa.Column('de2', sa.Boolean(), nullable=True),
    sa.Column('de3', sa.Boolean(), nullable=True),
    sa.Column('de4', sa.Boolean(), nullable=True),
    sa.Column('de5', sa.Boolean(), nullable=True),
    sa.Column('de6', sa.Boolean(), nullable=True),
    sa.Column('de7', sa.Boolean(), nullable=True),
    sa.Column('de8', sa.Boolean(), nullable=True),
    sa.Column('de9', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game3_date'), 'game3', ['date'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game3_date'), table_name='game3')
    op.drop_table('game3')
    op.drop_index(op.f('ix_game2_date'), table_name='game2')
    op.drop_table('game2')
    # ### end Alembic commands ###
