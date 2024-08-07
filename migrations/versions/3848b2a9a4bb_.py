"""empty message

Revision ID: 3848b2a9a4bb
Revises: d5b5112130b7
Create Date: 2024-08-06 22:17:12.479653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3848b2a9a4bb'
down_revision = 'd5b5112130b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__de1074fd')

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('latest_stage', sa.String(), nullable=True))

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d5290e62')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__01202f4b')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__01202f4b', ['date'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d5290e62', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.drop_column('latest_stage')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__de1074fd', ['hubspot_id'], unique=False)

    # ### end Alembic commands ###
