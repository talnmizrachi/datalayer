"""empty message

Revision ID: 5d68dd5e5d5c
Revises: 86cca2aab3c5
Create Date: 2024-10-15 11:53:35.037404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d68dd5e5d5c'
down_revision = '86cca2aab3c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('this_one_2')
    with op.batch_alter_table('tiktok_ads', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__05fa4234')

    op.drop_table('tiktok_ads')
    with op.batch_alter_table('_v2_oc_stats_combined', schema=None) as batch_op:
        batch_op.alter_column('cohort',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('_v2_oc_stats_from_rnd', schema=None) as batch_op:
        batch_op.alter_column('start_date',
               existing_type=sa.DATE(),
               nullable=False)

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__35958a48')

    with op.batch_alter_table('csat_submitted', schema=None) as batch_op:
        batch_op.alter_column('cohort',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=True)

    with op.batch_alter_table('csat_survey_event', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('facebook_fb_ads_insight_report_basic', schema=None) as batch_op:
        batch_op.drop_column('_rivery_run_id')

    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__f7da15d5')

    with op.batch_alter_table('google_ads_ad_performance_by_day', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__1fb314ce')

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__b77c718b')

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__91cda961')

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__d192fe96')

    with op.batch_alter_table('intercom_report_conversations', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__46910268')

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__474576b8')

    with op.batch_alter_table('tiktok_auction_ads_basic_daily', schema=None) as batch_op:
        batch_op.alter_column('dimensions_ad_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__2d74a561')

    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__6ef76449')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__6ef76449', ['campaign_id'], unique=False)

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__2d74a561', ['dimensions_stat_time_day', 'dimensions_campaign_id'], unique=False)

    with op.batch_alter_table('tiktok_auction_ads_basic_daily', schema=None) as batch_op:
        batch_op.alter_column('dimensions_ad_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__474576b8', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('intercom_report_conversations', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__46910268', ['id', 'created_at', 'updated_at'], unique=False)

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__d192fe96', ['adgroup_id', 'keywordview_resourcename', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__91cda961', ['campaign_id', 'segments_date', 'segments_device', 'segments_hour'], unique=False)

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__b77c718b', ['adgroupcriterion_criterionid', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_ad_performance_by_day', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__1fb314ce', ['adgroupad_ad_id', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__f7da15d5', ['adgroup_id', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('facebook_fb_ads_insight_report_basic', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_rivery_run_id', sa.VARCHAR(), autoincrement=False, nullable=True))

    with op.batch_alter_table('csat_survey_event', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('csat_submitted', schema=None) as batch_op:
        batch_op.alter_column('cohort',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__35958a48', ['hubspot_id'], unique=False)

    with op.batch_alter_table('_v2_oc_stats_from_rnd', schema=None) as batch_op:
        batch_op.alter_column('start_date',
               existing_type=sa.DATE(),
               nullable=True)

    with op.batch_alter_table('_v2_oc_stats_combined', schema=None) as batch_op:
        batch_op.alter_column('cohort',
               existing_type=sa.VARCHAR(),
               nullable=True)

    op.create_table('tiktok_ads',
    sa.Column('secondary_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deeplink', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ad_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('app_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('playable_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('profile_image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('advertiser_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('create_time', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image_mode', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ad_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('campaign_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('click_tracking_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('display_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ad_text', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('adgroup_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('video_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image_ids', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('landing_page_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('impression_tracking_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('modify_time', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('operation_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('call_to_action', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    with op.batch_alter_table('tiktok_ads', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__05fa4234', ['ad_id', 'campaign_id', 'advertiser_id', 'adgroup_id', 'video_id'], unique=False)

    op.create_table('this_one_2',
    sa.Column('Record ID', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('First Name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Last Name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
