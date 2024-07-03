"""Add rating and rating_count to Quote

Revision ID: d36af0db1ab9
Revises: 
Create Date: 2024-07-02 16:39:45.337239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd36af0db1ab9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rting_count', sa.Integer(), nullable=True))
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.drop_column('rting_count')

    # ### end Alembic commands ###
