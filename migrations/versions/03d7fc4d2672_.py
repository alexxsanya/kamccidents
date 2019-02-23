"""empty message

Revision ID: 03d7fc4d2672
Revises: d2f36ec6348e
Create Date: 2019-02-17 11:15:15.218863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03d7fc4d2672'
down_revision = 'd2f36ec6348e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accidents', 'acc_involved',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accidents', 'acc_involved',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###