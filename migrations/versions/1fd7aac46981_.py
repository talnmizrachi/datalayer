"""empty message

Revision ID: 1fd7aac46981
Revises: 1c50f641c96b
Create Date: 2024-06-16 23:17:22.867226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fd7aac46981'
down_revision = '1c50f641c96b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hubspot_current_deal_stage', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.drop_column('hubspot_current_deal_stage')

    # ### end Alembic commands ###
