"""empty message

Revision ID: a9425d6557f4
Revises: 
Create Date: 2021-03-27 15:11:01.172290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9425d6557f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Flight_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight', sa.String(length=64), nullable=False),
    sa.Column('airport_ori', sa.String(length=64), nullable=False),
    sa.Column('airport_des', sa.String(length=64), nullable=False),
    sa.Column('eta', sa.Integer(), nullable=False),
    sa.Column('anal_result', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=64), nullable=False),
    sa.Column('rvr', sa.Integer(), nullable=False),
    sa.Column('wind', sa.Integer(), nullable=False),
    sa.Column('cloud', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Weather')
    op.drop_table('User')
    op.drop_table('Flight_status')
    # ### end Alembic commands ###
