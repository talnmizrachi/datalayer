"""empty message

Revision ID: 88cc2f60a1e0
Revises: e07b338fa72a
Create Date: 2024-07-24 10:29:40.149652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88cc2f60a1e0'
down_revision = 'e07b338fa72a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('placement_revenue',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.drop_index('idx_rivery__0693b878')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__0693b878', ['date'], unique=False)
        batch_op.alter_column('placement_revenue',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
        batch_op.alter_column('date',
               existing_type=sa.String(),
               type_=sa.DATE(),
               existing_nullable=False)

    # ### end Alembic commands ###
