"""empty message

Revision ID: dac733e3d51f
Revises: 65b53d302ef6
Create Date: 2024-08-01 14:22:50.149132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dac733e3d51f'
down_revision = '65b53d302ef6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__553955ea')

    with op.batch_alter_table('bg_student_changes', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'bg_students', ['hubspot_id'], ['hubspot_id'])

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__ed0b0cdd')

    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__dbc14e87')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__03e0da37')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__03e0da37', ['date'], unique=False)

    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__dbc14e87', ['id', 'hubspot_id'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__ed0b0cdd', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('bg_student_changes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__553955ea', ['hubspot_id'], unique=False)

    # ### end Alembic commands ###
