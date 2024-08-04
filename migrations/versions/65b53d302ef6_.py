"""empty message

Revision ID: 65b53d302ef6
Revises: 0a37000073d7
Create Date: 2024-07-31 20:15:15.711839

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '65b53d302ef6'
down_revision = '0a37000073d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__572705d0')

    op.drop_table('google_ads_keyword_performance')
    with op.batch_alter_table('google_ads_ad_performance_by_day', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__68cd4bc8')

    op.drop_table('google_ads_ad_performance_by_day')
    with op.batch_alter_table('google_ads_ad_group_performance_by_hour', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__aeba0013')

    op.drop_table('google_ads_ad_group_performance_by_hour')
    with op.batch_alter_table('google_ads_geographic_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__c56cba4c')

    op.drop_table('google_ads_geographic_performance')
    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__96afec04')

    op.drop_table('google_ads_campaign_performance_by_hour')
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d975e689')

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stage_reason', sa.String(), nullable=True))

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__f4ee436f')

    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__3e1b1ae0')

    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__9b88e577')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v3_pulse_table', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__9b88e577', ['date'], unique=False)

    with op.batch_alter_table('student_new_payment', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__3e1b1ae0', ['id', 'hubspot_id'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__f4ee436f', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.drop_column('stage_reason')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d975e689', ['hubspot_id', 'type_of_collection_code', 'created_at'], unique=False)

    op.create_table('google_ads_campaign_performance_by_hour',
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_currencycode', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_descriptivename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurablecostmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurableimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewviewability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_clicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_conversions', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_conversionsvalue', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_costmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_impressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_interactioneventtypes', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('metrics_interactions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_viewthroughconversions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('segments_adnetworktype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('segments_device', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_hour', sa.INTEGER(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__96afec04', ['campaign_id', 'segments_date', 'segments_device', 'segments_hour'], unique=False)

    op.create_table('google_ads_geographic_performance',
    sa.Column('adgroup_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_currencycode', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_descriptivename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('geographicview_countrycriterionid', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('geographicview_locationtype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metrics_clicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_conversions', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_conversionsvalue', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_costmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_impressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_interactioneventtypes', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('metrics_interactions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_viewthroughconversions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('segments_adnetworktype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('segments_device', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_geotargetcity', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_geotargetregion', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('google_ads_geographic_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__c56cba4c', ['adgroup_id', 'geographicview_countrycriterionid', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    op.create_table('google_ads_ad_group_performance_by_hour',
    sa.Column('adgroup_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_currencycode', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_descriptivename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurablecostmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurableimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewviewability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_clicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_conversions', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_conversionsvalue', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_costmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_impressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_interactioneventtypes', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('metrics_interactions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_viewthroughconversions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('segments_adnetworktype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('segments_device', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_hour', sa.INTEGER(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('google_ads_ad_group_performance_by_hour', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__aeba0013', ['adgroup_id', 'segments_adnetworktype', 'segments_date', 'segments_device', 'segments_hour'], unique=False)

    op.create_table('google_ads_ad_performance_by_day',
    sa.Column('adgroupad_ad_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroupad_ad_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_currencycode', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_descriptivename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurablecostmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurableimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewviewability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_clicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_conversions', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_conversionsvalue', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_costmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_impressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_interactioneventtypes', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('metrics_interactions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_viewthroughconversions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('segments_adnetworktype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('segments_device', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('google_ads_ad_performance_by_day', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__68cd4bc8', ['adgroupad_ad_id', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    op.create_table('google_ads_keyword_performance',
    sa.Column('adgroupcriterion_finalurls', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('adgroupcriterion_keyword_matchtype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroupcriterion_keyword_text', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroupcriterion_qualityinfo_qualityscore', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('adgroup_finalurlsuffix', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_resourcename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_currencycode', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_descriptivename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('keywordview_resourcename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurablecostmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewmeasurableimpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_activeviewviewability', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_clicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_conversions', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_conversionsvalue', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_costmicros', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_impressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_interactioneventtypes', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('metrics_interactions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('metrics_searchimpressionshare', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('metrics_viewthroughconversions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('segments_adnetworktype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('segments_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('segments_device', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__572705d0', ['adgroup_id', 'keywordview_resourcename', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    # ### end Alembic commands ###