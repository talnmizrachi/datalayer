from db import db


class TiktokAuctionAdsBasicDaily(db.Model):
    __tablename__ = 'tiktok_auction_ads_basic_daily'

    metrics_impressions = db.Column(db.String)
    metrics_clicks = db.Column(db.String)
    metrics_spend = db.Column(db.String)
    dimensions_stat_time_day = db.Column(db.String)
    dimensions_ad_id = db.Column(db.String, primary_key=True)

    __table_args__ = (
        db.Index('idx_rivery__64eb382d', 'dimensions_stat_time_day', 'dimensions_ad_id'),
    )
