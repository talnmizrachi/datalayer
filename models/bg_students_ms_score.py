from db import db
from uuid import uuid4


class BGStudentMSScoreModel(db.Model):
    __tablename__ = 'bg_students_ms_score'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    date_of_review = db.Column(db.Date, nullable=False)
    hubspot_id = db.Column(db.String, nullable=False), db.ForeignKey('bg_students.hubspot_id')
    cohort = db.Column(db.String, nullable=False)
    domain = db.Column(db.String, nullable=False)
    instruction = db.Column(db.Integer, nullable=True)
    mentorship = db.Column(db.Integer, nullable=True)
    curriculum = db.Column(db.Integer, nullable=True)
    success_support = db.Column(db.Integer, nullable=True)
    placement_support = db.Column(db.Integer, nullable=True)
    overall_experience = db.Column(db.Integer, nullable=True)
    ratio = db.Column(db.String, nullable=True)
    final_score = db.Column(db.Float, nullable=True)
