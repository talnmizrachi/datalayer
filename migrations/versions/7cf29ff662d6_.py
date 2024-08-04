"""empty message

Revision ID: 7cf29ff662d6
Revises: 331ec2b52f22
Create Date: 2024-08-04 10:15:10.751315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cf29ff662d6'
down_revision = '331ec2b52f22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d0d58313')

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__6742b7da')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__e9af3461')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__e9af3461', ['date'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__6742b7da', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('email')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d0d58313', ['hubspot_id'], unique=False)

    # ### end Alembic commands ###
