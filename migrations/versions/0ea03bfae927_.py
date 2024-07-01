"""empty message

Revision ID: 0ea03bfae927
Revises: bc09ef45a378
Create Date: 2024-07-01 13:00:15.090312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea03bfae927'
down_revision = 'bc09ef45a378'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_owner', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.drop_column('student_owner')

    # ### end Alembic commands ###