from db import db
from uuid import uuid4


class JobReadyStudentModel(db.Model):
    __tablename__ = 'job_ready_students'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    student_ms_id = db.Column(db.String, nullable=True)
    hubspot_id = db.Column(db.String, nullable=False, unique=True)
    
    domain = db.Column(db.String, nullable=True)
    active_cohort = db.Column(db.String, nullable=True)
    
    student_first_name = db.Column(db.String, nullable=True)
    student_last_name = db.Column(db.String, nullable=True)

    schoolmaster_id = db.Column(db.String, nullable=True)
    
    is_employed = db.Column(db.Boolean, nullable=False, default=False)
    
    student_owner = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    current_program = db.Column(db.String, default='deferred')
    hubspot_current_deal_stage = db.Column(db.String, nullable=True)
