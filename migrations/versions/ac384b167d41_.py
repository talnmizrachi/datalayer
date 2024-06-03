"""empty message

Revision ID: ac384b167d41
Revises: 983118d18a95
Create Date: 2024-06-03 16:26:11.399943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac384b167d41'
down_revision = '983118d18a95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_timestamp', sa.DateTime(), nullable=False))

    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('is_closed_won',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('is_closed_won',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    with op.batch_alter_table('job_ready_students', schema=None) as batch_op:
        batch_op.drop_column('updated_timestamp')

    # ### end Alembic commands ###
