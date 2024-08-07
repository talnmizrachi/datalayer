"""empty message

Revision ID: 74d3f2898965
Revises: f41ae559073f
Create Date: 2024-08-05 18:45:46.003953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74d3f2898965'
down_revision = 'f41ae559073f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__cf108c07')

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('student_last_name', sa.String(), nullable=True))

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__a62a857d')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__516ad86b')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__516ad86b', ['date'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__a62a857d', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.drop_column('student_last_name')
        batch_op.drop_column('student_first_name')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__cf108c07', ['hubspot_id'], unique=False)

    # ### end Alembic commands ###
