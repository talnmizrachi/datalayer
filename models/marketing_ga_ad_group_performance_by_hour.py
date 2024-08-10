from db import db


class MarketingGoogleAdGroupPerformanceByHour(db.Model):
    __tablename__ = 'google_ads_ad_group_performance_by_hour'
    
    customer_currencycode = db.Column(db.String)
    customer_descriptivename = db.Column(db.String)
    customer_id = db.Column(db.String, primary_key=True)
    metrics_activeviewimpressions = db.Column(db.Integer)
    metrics_activeviewmeasurability = db.Column(db.Float)
    metrics_activeviewmeasurablecostmicros = db.Column(db.Integer)
    metrics_activeviewmeasurableimpressions = db.Column(db.Integer)
    metrics_activeviewviewability = db.Column(db.Float)
    metrics_allconversions = db.Column(db.Float)
    metrics_allconversionsvalue = db.Column(db.Float)
    metrics_clicks = db.Column(db.Integer)
    metrics_costmicros = db.Column(db.Integer)
    metrics_impressions = db.Column(db.Integer)
    metrics_interactioneventtypes = db.Column(db.JSON)
    metrics_interactions = db.Column(db.Integer)
    metrics_viewthroughconversions = db.Column(db.Integer)
    segments_adnetworktype = db.Column(db.String)
    segments_date = db.Column(db.Date)
    segments_device = db.Column(db.String)
    segments_hour = db.Column(db.Integer)