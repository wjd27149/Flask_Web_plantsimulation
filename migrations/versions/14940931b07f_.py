"""empty message

Revision ID: 14940931b07f
Revises: 78491f1a7b51
Create Date: 2024-10-08 02:09:21.646796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14940931b07f'
down_revision = '78491f1a7b51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_machine',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.Float(), nullable=True),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('material', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('time')
    )
    op.create_table('material',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.Float(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('machine', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('material')
    op.drop_table('base_machine')
    # ### end Alembic commands ###
