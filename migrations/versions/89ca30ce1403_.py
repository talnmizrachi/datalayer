"""empty message

Revision ID: 89ca30ce1403
Revises: 01fa0fe17238
Create Date: 2024-06-03 22:51:28.557690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89ca30ce1403'
down_revision = '01fa0fe17238'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source_1', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('source_2', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.drop_column('source_2')
        batch_op.drop_column('source_1')

    # ### end Alembic commands ###
