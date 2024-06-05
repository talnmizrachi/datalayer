from db import db
from uuid import uuid4


class Process(db.Model):
    """
    A process object is the unique combination of company-title-student

    """
    __tablename__ = 'processes'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    job_id = db.Column(db.String, nullable=False, default=lambda: str(uuid4().hex))
    # add constraint to make sure student_id is either student_id or job_ready or regular student
    student_id = db.Column(db.String,  nullable=False)
    
    student_firstname = db.Column(db.String, nullable=False)
    student_lastname = db.Column(db.String, nullable=False)
    domain = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    
    company_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String, nullable=False)
    
    drive_url = db.Column(db.String, nullable=True)
    cv_url = db.Column(db.String, nullable=False)
    process_start_date = db.Column(db.DateTime, nullable=False)
    process_end_date = db.Column(db.DateTime, nullable=True)
    
    is_process_active = db.Column(db.Boolean, nullable=False, default=True)
    is_closed_won = db.Column(db.Boolean, nullable=True)
    
    source_1 = db.Column(db.String, nullable=True)
    source_2 = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())