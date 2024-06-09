from db import db
from uuid import uuid4


class MockInterviewModel(db.Model):
    __tablename__ = 'mock_interviews'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    stage_id = db.Column(db.String, db.ForeignKey('process_stage.id'), nullable=False)
    process_id = db.Column(db.String, db.ForeignKey('processes.id'), nullable=False)
    
    mentor_id = db.Column(db.String, db.ForeignKey('mentors.id'))
    mentor_name = db.Column(db.String, nullable=True)
    mentor_email = db.Column(db.String, nullable=True)
    
    stage_in_funnel = db.Column(db.String, nullable=True)
    type_of_stage = db.Column(db.String, nullable=True)
    stage_date = db.Column(db.Date, nullable=True)
    
    had_home_assignment = db.Column(db.Boolean, nullable=True)
    home_assignment_questions = db.Column(db.String, nullable=True)
    home_assignment_answers = db.Column(db.String, nullable=True)
    
    mock_interview_datetime = db.Column(db.DateTime, nullable=True)
    questions_doc_link = db.Column(db.String, nullable=True)
    mock_interview_feedback_id = db.Column(db.String, nullable=True)
    mock_interview_recording_link = db.Column(db.String, nullable=True)
    student_nps = db.Column(db.Integer, nullable=True)
    additional_details = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())