"""empty message

Revision ID: 83d268cbdb89
Revises: 94f1d784483b
Create Date: 2024-09-13 09:28:16.569767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83d268cbdb89'
down_revision = '94f1d784483b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__e62f2931')

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__c6f30cbe')

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__61618dab')

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__a9677fe2')

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d3110260')

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__74dd73f7')

    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d88d77f7')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.alter_column('placement_revenue',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.BigInteger(),
               existing_nullable=True)
        batch_op.alter_column('monthly_placements_revenue',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.BigInteger(),
               existing_nullable=True)
        batch_op.alter_column('yearly_placements_revenue',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.BigInteger(),
               existing_nullable=True)
        batch_op.alter_column('quarterly_placements_revenue',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.BigInteger(),
               existing_nullable=True)
        batch_op.drop_column('monthly_cummulative_placements')
        batch_op.drop_column('yearly_cummulative_placements')
        batch_op.drop_column('cummulative_monthly_applications')
        batch_op.drop_column('quarterly_cummulative_placements')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quarterly_cummulative_placements', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('cummulative_monthly_applications', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('yearly_cummulative_placements', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('monthly_cummulative_placements', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('quarterly_placements_revenue',
               existing_type=sa.BigInteger(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
        batch_op.alter_column('yearly_placements_revenue',
               existing_type=sa.BigInteger(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
        batch_op.alter_column('monthly_placements_revenue',
               existing_type=sa.BigInteger(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
        batch_op.alter_column('placement_revenue',
               existing_type=sa.BigInteger(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)

    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d88d77f7', ['campaign_id'], unique=False)

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__74dd73f7', ['dimensions_stat_time_day', 'dimensions_campaign_id'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d3110260', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__a9677fe2', ['adgroup_id', 'keywordview_resourcename', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__61618dab', ['campaign_id', 'segments_date', 'segments_device', 'segments_hour'], unique=False)

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__c6f30cbe', ['adgroupcriterion_criterionid', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__e62f2931', ['adgroup_id', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    # ### end Alembic commands ###