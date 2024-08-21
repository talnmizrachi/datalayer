from db import db


class TiktokCampaigns(db.Model):
    __tablename__ = 'tiktok_campaigns'

    campaign_id = db.Column(db.String, primary_key=True)
    campaign_name = db.Column(db.String)