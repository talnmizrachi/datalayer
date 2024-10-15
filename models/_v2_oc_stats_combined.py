from db import db

class V2OcStatsCombined(db.Model):
    __tablename__ = '_v2_oc_stats_combined'

    cohort = db.Column(db.String, primary_key=True)
    recommendation_rate = db.Column(db.Float)
    positive_recommendation = db.Column(db.Integer)
    negative_recommendations = db.Column(db.Integer)
    drops__not_included_ = db.Column(db.Integer)
    amount_students_enrolled = db.Column(db.Integer)
    amount_students_at_end = db.Column(db.Integer)

    __table_args__ = {'schema': 'public'}
