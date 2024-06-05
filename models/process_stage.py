from db import db
from uuid import uuid4


class StageModel(db.Model):
    __tablename__ = 'process_stage'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    process_id = db.Column(db.String, db.ForeignKey('processes.id'), nullable=False)
    student_firstname = db.Column(db.String, nullable=False)
    student_lastname = db.Column(db.String, nullable=False)
    stage_in_funnel = db.Column(db.String, nullable=False)
    type_of_stage = db.Column(db.String, nullable=False)
    had_home_assignment = db.Column(db.Boolean, nullable=False, default=False)
    home_assignment_questions = db.Column(db.String, nullable=True)
    home_assignment_answers = db.Column(db.String, nullable=True)
    is_pass = db.Column(db.String, nullable=False, default="PENDING")
    stage_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
