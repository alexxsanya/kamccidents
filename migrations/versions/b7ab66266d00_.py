"""empty message

Revision ID: b7ab66266d00
Revises: 03d7fc4d2672
Create Date: 2019-02-17 11:18:30.672991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7ab66266d00'
down_revision = '03d7fc4d2672'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accidents', 'acc_involved',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accidents', 'acc_involved',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###
