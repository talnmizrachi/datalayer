from db import db

class CSATSurveyEvent(db.Model):
    __tablename__ = 'csat_survey_event'

    event = db.Column(db.String)
    event_text = db.Column(db.String)
    id = db.Column(db.String, primary_key=True)
    pulse_date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    hubspot_id = db.Column(db.String)

    __table_args__ = (
        db.Index('idx_rivery__204877d5', 'event', 'event_text', 'id', 'hubspot_id'),
    )
