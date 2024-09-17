from db import db


class V2MSScore(db.Model):
    __tablename__ = 'v2_ms_score'

    hubspot_id = db.Column(db.String)
    type = db.Column(db.String)
    poc = db.Column(db.String)
    survey_date = db.Column(db.Date)
    domain = db.Column(db.String)
    active_cohort = db.Column(db.String)
    rating = db.Column(db.Integer)
    row_id = db.Column(db.String, primary_key=True)

    __table_args__ = (
        db.Index('idx_rivery__21e4f819', 'hubspot_id', 'type', 'poc', 'survey_date', 'domain', 'active_cohort'),
    )
    
    