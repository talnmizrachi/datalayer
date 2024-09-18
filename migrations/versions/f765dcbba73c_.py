"""empty message

Revision ID: f765dcbba73c
Revises: 83d268cbdb89
Create Date: 2024-09-17 19:41:54.565570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f765dcbba73c'
down_revision = '83d268cbdb89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__10e643cf')

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plan_location', sa.String(), nullable=True))

    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__57727bae')

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__89d01dfa')

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__3721b551')

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__a6b1e1ad')

    with op.batch_alter_table('intercom_report_conversations', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__c6c56c45')

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__23ba6718')

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__ccf30fc5')

    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.drop_index('idx_rivery__b51b4579')

    with op.batch_alter_table('v2_ms_score', schema=None) as batch_op:
        batch_op.alter_column('row_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('v2_ms_score', schema=None) as batch_op:
        batch_op.alter_column('row_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('tiktok_campaigns', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__b51b4579', ['campaign_id'], unique=False)

    with op.batch_alter_table('tiktok_auction_ads_campaign_basic_daily', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__ccf30fc5', ['dimensions_stat_time_day', 'dimensions_campaign_id'], unique=False)

    with op.batch_alter_table('student_applications', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__23ba6718', ['student_id', 'student_response_timestamp', 'source', 'id'], unique=False)

    with op.batch_alter_table('intercom_report_conversations', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__c6c56c45', ['id', 'created_at', 'updated_at'], unique=False)

    with op.batch_alter_table('google_ads_keyword_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__a6b1e1ad', ['adgroup_id', 'keywordview_resourcename', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_campaign_performance_by_hour', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__3721b551', ['campaign_id', 'segments_date', 'segments_device', 'segments_hour'], unique=False)

    with op.batch_alter_table('google_ads_audience_performance', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__89d01dfa', ['adgroupcriterion_criterionid', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('google_ads_ad_group_performance_by_day', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__57727bae', ['adgroup_id', 'segments_adnetworktype', 'segments_date', 'segments_device'], unique=False)

    with op.batch_alter_table('bg_students', schema=None) as batch_op:
        batch_op.drop_column('plan_location')

    with op.batch_alter_table('another_payments_test_1', schema=None) as batch_op:
        batch_op.create_index('idx_rivery__10e643cf', ['hubspot_id'], unique=False)

    # ### end Alembic commands ###