from db import db
from uuid import uuid4


class MockInterviewModel(db.Model):
    __tablename__ = 'mock_interviews'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    stage_id = db.Column(db.String, db.ForeignKey('process_stage.id'), nullable=False)
    process_id = db.Column(db.String, db.ForeignKey('processes.id'), nullable=False)
    
    mentor_email = db.Column(db.String, nullable=True)
    
    stage_in_funnel = db.Column(db.String, nullable=True)
    type_of_stage = db.Column(db.String, nullable=True)
    stage_date = db.Column(db.Date, nullable=True)
    
    mock_interview_datetime = db.Column(db.DateTime, nullable=True)
    student_nps = db.Column(db.Integer, nullable=True)
    additional_details = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())