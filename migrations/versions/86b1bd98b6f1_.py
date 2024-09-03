"""empty message

Revision ID: 86b1bd98b6f1
Revises: cfe75dd7b194
Create Date: 2024-09-03 11:15:46.016663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86b1bd98b6f1'
down_revision = 'cfe75dd7b194'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('process_stage', schema=None) as batch_op:
        batch_op.alter_column('stage_date',
               existing_type=sa.DATE(),
               nullable=True)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__b349ca91')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__edbc368e')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__edbc368e', ['date'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__b349ca91', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('process_stage', schema=None) as batch_op:
        batch_op.alter_column('stage_date',
               existing_type=sa.DATE(),
               nullable=False)

    # ### end Alembic commands ###
