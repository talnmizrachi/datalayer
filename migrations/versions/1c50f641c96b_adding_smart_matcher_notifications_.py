"""adding smart matcher notifications cancelling nulls

Revision ID: 1c50f641c96b
Revises: 9943937e0fae
Create Date: 2024-06-16 10:53:24.935598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c50f641c96b'
down_revision = '9943937e0fae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.alter_column('smart_matcher_notification',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.alter_column('smart_matcher_notification',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###