from db import db


class MarketingGoogleAdsAudiencePerformance(db.Model):
    __tablename__ = 'google_ads_audience_performance'
    
    adgroupcriterion_criterionid = db.Column(db.String, primary_key=True)
    adgroup_id = db.Column(db.String)
    adgroup_name = db.Column(db.String)
    campaign_id = db.Column(db.String)
    campaign_name = db.Column(db.String)
    customer_currencycode = db.Column(db.String)
    customer_descriptivename = db.Column(db.String)
    customer_id = db.Column(db.String)
    metrics_activeviewimpressions = db.Column(db.Integer)
    metrics_activeviewmeasurability = db.Column(db.Float)
    metrics_activeviewmeasurablecostmicros = db.Column(db.Integer)
    metrics_activeviewmeasurableimpressions = db.Column(db.Integer)
    metrics_activeviewviewability = db.Column(db.Float)
    metrics_clicks = db.Column(db.Integer)
    metrics_conversions = db.Column(db.Float)
    metrics_conversionsvalue = db.Column(db.Float)
    metrics_costmicros = db.Column(db.Integer)
    metrics_impressions = db.Column(db.Integer)
    metrics_interactioneventtypes = db.Column(db.JSON)
    metrics_interactions = db.Column(db.Integer)
    metrics_viewthroughconversions = db.Column(db.Integer)
    segments_adnetworktype = db.Column(db.String)
    segments_date = db.Column(db.Date)
    segments_device = db.Column(db.String)
