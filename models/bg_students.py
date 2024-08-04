from db import db
from uuid import uuid4


class BGStudentModel(db.Model):
    __tablename__ = 'bg_students'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    enrolment_pipeline_stage = db.Column(db.String, nullable=True)
    stage_reason = db.Column(db.String, nullable=True)
    hubspot_id = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True, unique=True)
    domain = db.Column(db.String, nullable=True)
    active_cohort = db.Column(db.String, nullable=True)
    hs_pipeline = db.Column(db.String, nullable=True)
    is_employed = db.Column(db.Boolean, nullable=False, default=False)
    
    student_owner = db.Column(db.String, nullable=True)

    is_job_ready = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

