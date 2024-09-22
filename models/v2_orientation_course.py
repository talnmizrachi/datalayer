from db import db


class V2OC2FPStatus(db.Model):
    __tablename__ = "v2_oc2fp"

    deal_id = db.Column(db.String, primary_key=True, nullable=False)
    hubspot_id = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    closed_lost_reason = db.Column(db.String)
    enrollment_cohort = db.Column(db.Date)
    bg_disapproval_reason = db.Column(db.String)
    dealstage = db.Column(db.String)
    closed_date = db.Column(db.Date)
