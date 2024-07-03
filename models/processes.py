from db import db
from uuid import uuid4


class ProcessModel(db.Model):
    """
    A process object is the unique combination of company-title-student

    """
    __tablename__ = 'processes'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    job_id = db.Column(db.String, nullable=False, default=lambda: str(uuid4().hex))
    hubspot_id = db.Column(db.String, nullable=True)
    # add constraint to make sure student_id is either student_id or job_ready or regular student
    student_ms_id = db.Column(db.String, nullable=True)
    student_id = db.Column(db.String,  nullable=False)
    
    domain = db.Column(db.String, nullable=False)
    
    company_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    
    #notification of starting a process
    process_start_date = db.Column(db.Date, nullable=False)
    #notification of failure / notification of success
    process_end_date = db.Column(db.Date, nullable=True)
    
    is_process_active = db.Column(db.Boolean, nullable=False, default=True)
    is_closed_won = db.Column(db.Boolean, nullable=True)
    
    source_1 = db.Column(db.String, nullable=True)
    source_2 = db.Column(db.String, nullable=True)
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    job_secured_date = db.Column(db.Date, nullable=True)
    
