from db import db

class FacebookFbAdsCampaigns(db.Model):
    __tablename__ = 'facebook_fb_ads_campaigns'

    _is_skadnetwork_attribution = db.Column(db.Boolean)
    _budget_remaining = db.Column(db.String)
    _objective = db.Column(db.String)
    _updated_time = db.Column(db.String)
    _can_create_brand_lift_study = db.Column(db.Boolean)
    _topline_id = db.Column(db.String)
    _created_time = db.Column(db.String)
    _special_ad_category = db.Column(db.String)
    _lifetime_budget = db.Column(db.String)
    _campaign_id = db.Column(db.String, primary_key=True)
    _stop_time = db.Column(db.String)
    _status = db.Column(db.String)
    _account_id = db.Column(db.String)
    _start_time = db.Column(db.String)
    _configured_status = db.Column(db.String)
    _buying_type = db.Column(db.String)
    _budget_rebalance_flag = db.Column(db.Boolean)
    _source_campaign_id = db.Column(db.String)
    _source_campaign = db.Column(db.JSON)
    _effective_status = db.Column(db.String)
    _campagin_name = db.Column(db.String)
    _bid_strategy = db.Column(db.String)
    _can_use_spend_cap = db.Column(db.Boolean)
    _smart_promotion_type = db.Column(db.String)

    __table_args__ = (
        db.Index('idx_rivery__c0d113c8', '_campaign_id', '_account_id'),
    )
