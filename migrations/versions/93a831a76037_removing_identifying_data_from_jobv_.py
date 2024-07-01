"""removing identifying data from jobv_ready_students

Revision ID: 93a831a76037
Revises: 26e2ef8095e4
Create Date: 2024-07-01 09:56:06.897145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a831a76037'
down_revision = '26e2ef8095e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_master_id', sa.String(), nullable=True))
        batch_op.drop_column('tags')
        batch_op.drop_column('jaq')
        batch_op.drop_column('school_master_name')

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.drop_column('student_lastname')
        batch_op.drop_column('email_address')
        batch_op.drop_column('cv_url')
        batch_op.drop_column('drive_url')
        batch_op.drop_column('student_firstname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_firstname', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('drive_url', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('cv_url', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('student_lastname', sa.VARCHAR(), autoincrement=False, nullable=False))

    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_master_name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('jaq', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('tags', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('school_master_id')

    # ### end Alembic commands ###
