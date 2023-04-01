"""empty message

Revision ID: f7a20f99d0ef
Revises: b9c7cc845174
Create Date: 2023-04-01 15:03:15.144702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7a20f99d0ef'
down_revision = 'b9c7cc845174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=1000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=500),
               existing_nullable=False)

    # ### end Alembic commands ###
