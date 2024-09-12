from db import db


class CSATSubmitted(db.Model):
    __tablename__ = 'csat_submitted'
    
    row_id = db.Column(db.String, primary_key=True)
    event_text = db.Column(db.String)
    hubspot_id = db.Column(db.String)
    rating = db.Column(db.Integer)
    sent_at = db.Column(db.DateTime)
    type = db.Column(db.String)
    mentor_full_name = db.Column(db.String)
    instructor_name = db.Column(db.String)

    __table_args__ = (
        db.Index('idx_rivery__263852dc', 'event_text', 'hubspot_id', 'type'),
    )
