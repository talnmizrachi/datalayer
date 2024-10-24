from db import db

class FacebookFbAdsInsightReportBasic(db.Model):
    __tablename__ = 'facebook_fb_ads_insight_report_basic'

    _spend = db.Column(db.String)
    _unique_ctr = db.Column(db.String)
    _account_name = db.Column(db.String)
    _campaign_id = db.Column(db.String)
    _clicks = db.Column(db.String)
    _video_p50_watched_actions = db.Column(db.JSON)
    _video_p100_watched_actions = db.Column(db.JSON)
    _video_p25_watched_actions = db.Column(db.JSON)
    _ctr = db.Column(db.String)
    _reach = db.Column(db.String)
    _cpm = db.Column(db.String)
    _date_start = db.Column(db.String)
    _video_p75_watched_actions = db.Column(db.JSON)
    _adset_name = db.Column(db.String)
    _video_avg_time_watched_actions = db.Column(db.JSON)
    _impressions = db.Column(db.String)
    _unique_actions = db.Column(db.JSON)
    _ad_id = db.Column(db.String, primary_key=True)
    _cpp = db.Column(db.String)
    _adset_id = db.Column(db.String)
    _actions = db.Column(db.JSON)
    _ad_name = db.Column(db.String)
    _frequency = db.Column(db.String)
    _social_spend = db.Column(db.String)
    _date_stop = db.Column(db.String)
    _cpc = db.Column(db.String)
    _unique_clicks = db.Column(db.String)
    _video_p95_watched_actions = db.Column(db.JSON)
    _account_id = db.Column(db.String)
    _campaign_name = db.Column(db.String)
    _cost_per_action_type = db.Column(db.JSON)
    _currency = db.Column(db.String)
    _conversions = db.Column(db.JSON)
    _inline_link_clicks = db.Column(db.String)
    _unique_inline_link_clicks = db.Column(db.String)
    _unique_link_clicks_ctr = db.Column(db.String)
    _cost_per_conversion = db.Column(db.JSON)
    _outbound_clicks = db.Column(db.JSON)
    _unique_outbound_clicks = db.Column(db.JSON)
    _outbound_clicks_ctr = db.Column(db.JSON)
    _unique_inline_link_click_ctr = db.Column(db.String)
    _unique_outbound_clicks_ctr = db.Column(db.JSON)
    _rivery_last_update = db.Column(db.DateTime)
    _rivery_river_id = db.Column(db.String)
    _rivery_run_id = db.Column(db.String)

    __table_args__ = (
        db.Index('idx_rivery__86770e08', '_campaign_id', '_date_start', '_ad_id', '_adset_id', '_account_id'),
    )




