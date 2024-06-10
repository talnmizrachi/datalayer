"""empty message

Revision ID: 631e7f73676c
Revises: 64a1d0609ab5
Create Date: 2024-06-08 01:54:21.823190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631e7f73676c'
down_revision = '64a1d0609ab5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mock_interviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mentor_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('mentor_email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('stage_in_funnel', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('type_of_stage', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('additional_details', sa.String(), nullable=True))
        batch_op.drop_column('mentor')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mock_interviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mentor', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('additional_details')
        batch_op.drop_column('type_of_stage')
        batch_op.drop_column('stage_in_funnel')
        batch_op.drop_column('mentor_email')
        batch_op.drop_column('mentor_name')

    # ### end Alembic commands ###