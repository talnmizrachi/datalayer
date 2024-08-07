"""empty message

Revision ID: ceab62691071
Revises: 4606f253e822
Create Date: 2024-07-23 11:11:06.646143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceab62691071'
down_revision = '4606f253e822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('payments_test')
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_index('idx_rivery__595d1305')

    with op.batch_alter_table('student_deal_stages', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('student_deal_stages', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__595d1305', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    op.create_table('payments_test',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_createdate', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_current_enrollment_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_first_actual_payment_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_hs_object_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_lastmodifieddate', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('properties_tuition_after_discount__usd_', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('createdat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updatedat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('archived', sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
