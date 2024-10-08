"""empty message

Revision ID: 6d42a7c70340
Revises: c5b51d551ef5
Create Date: 2024-09-19 08:53:50.485826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d42a7c70340'
down_revision = 'c5b51d551ef5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.drop_column('is_job_ready')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_job_ready', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
