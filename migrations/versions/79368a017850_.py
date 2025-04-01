"""empty message

Revision ID: 79368a017850
Revises: af33749d3629
Create Date: 2025-04-01 17:13:03.974680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '79368a017850'
down_revision = 'af33749d3629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('publisher')
    # op.drop_table('book')
    # op.drop_table('author')
    # op.drop_table('book_publisher')
    with op.batch_alter_table('operation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('o_name', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('operation', schema=None) as batch_op:
        batch_op.drop_column('o_name')

    op.create_table('book_publisher',
    sa.Column('book_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('publisher_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], name='book_publisher_ibfk_1'),
    sa.ForeignKeyConstraint(['publisher_id'], ['publisher.id'], name='book_publisher_ibfk_2'),
    sa.PrimaryKeyConstraint('book_id', 'publisher_id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_table('author',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('age', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sex', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('email', mysql.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_table('book',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='book_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_table('publisher',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('address', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('city', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('province', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('country', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('website', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
