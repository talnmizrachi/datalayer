from db import db
from uuid import uuid4


class BGStudentModel2(db.Model):
    __tablename__ = 'bg_students_2'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    source = db.Column(db.String, nullable=False) #enrollment or deal
    
    enrolment_pipeline_stage = db.Column(db.String, nullable=True)
    hubspot_id = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True, unique=True)
    
    active_cohort = db.Column(db.String, nullable=True)
    domain = db.Column(db.String, nullable=True)
    plan_duration = db.Column(db.String, nullable=True)
    plan_location = db.Column(db.String, nullable=True)
    
    enrollment_id = db.Column(db.String, nullable=True)
    
    hs_pipeline = db.Column(db.String, nullable=True)
    is_employed = db.Column(db.Boolean, nullable=False, default=False)

    student_owner = db.Column(db.String, nullable=True)
    is_job_ready = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    object_modified = db.Column(db.DateTime, nullable=False) #the timestamp the record actually was modified
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

