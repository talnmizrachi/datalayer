"""empty message

Revision ID: 721e8882885a
Revises: de18e7f2ddfd
Create Date: 2024-07-02 14:48:36.497340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '721e8882885a'
down_revision = 'de18e7f2ddfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('process_stage', schema=None) as batch_op:
        batch_op.drop_column('home_assignment_answers')
        batch_op.drop_column('home_assignment_questions')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('process_stage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_assignment_questions', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('home_assignment_answers', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###