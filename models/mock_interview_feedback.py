from db import db
from uuid import uuid4


class MockInterviewFeedbackModel(db.Model):
    __tablename__ = 'mock_interview_feedback'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    stage_id = db.Column(db.String, db.ForeignKey('mock_interviews.id'), nullable=False, unique=False)
    mentor_id = db.Column(db.String, db.ForeignKey('mentors.id'), unique=False)
    student_id = db.Column(db.String, nullable=False)
    mentor_name = db.Column(db.String)
    
    gen_dem_feedback = db.Column(db.String, nullable=True)
    comm_feedback = db.Column(db.String, nullable=True)
    analytical_feedback = db.Column(db.String, nullable=True)
    tech_feedback = db.Column(db.String, nullable=True)
    homework = db.Column(db.String, nullable=True)
    domain_feedback = db.Column(db.String, nullable=True)
    pitch_feedback = db.Column(db.String, nullable=True)
    past_project_feedback = db.Column(db.String, nullable=True)
    internal_notes = db.Column(db.String, nullable=True)
    overall_rating = db.Column(db.Float, nullable=True)
    mentor_email = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
