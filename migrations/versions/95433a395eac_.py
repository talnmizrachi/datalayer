"""empty message

Revision ID: 95433a395eac
Revises: 0ea03bfae927
Create Date: 2024-07-01 14:13:13.276061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95433a395eac'
down_revision = '0ea03bfae927'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('career_success_advisors')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('career_success_advisors',
    sa.Column('csa_fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('csa_email', sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    # ### end Alembic commands ###