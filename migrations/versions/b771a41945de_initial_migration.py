"""Initial migration

Revision ID: b771a41945de
Revises: 
Create Date: 2024-06-16 10:35:37.884943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b771a41945de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('csa_fullname', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.drop_column('csa_fullname')

    # ### end Alembic commands ###
