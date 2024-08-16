from db import db
from uuid import uuid4


class MarketingMqlStudentsModel(db.Model):
    __tablename__ = 'marketing_mql_students'
    
    hubspot_id = db.Column(db.String, primary_key=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    
    mql_score = db.Column(db.Integer)
    
    utm_campaign = db.Column(db.String)
    utm_source = db.Column(db.String)
    utm_medium = db.Column(db.String)
    utm_content = db.Column(db.String)
    utm_id = db.Column(db.String)
    utm_term = db.Column(db.String)
    
    date_mql_entered = db.Column(db.DateTime)
    hubspot_created_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    