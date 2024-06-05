from db import db
from uuid import uuid4


class JobReadyStudentModel(db.Model):
    __tablename__ = 'job_ready_students'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    masterschool_id = db.Column(db.String, nullable=False, unique=True)
    hubspot_id = db.Column(db.Integer, nullable=False, unique=True)
    
    domain = db.Column(db.String, nullable=False)
    
    student_firstname = db.Column(db.String, nullable=False)
    student_lastname = db.Column(db.String, nullable=False)
    student_email = db.Column(db.String, nullable=False)
    
    student_country = db.Column(db.String, nullable=False)
    student_state = db.Column(db.String, nullable=True)
    student_city = db.Column(db.String, nullable=False)
    
    student_github_link = db.Column(db.String, nullable=True)
    student_linkedin_link = db.Column(db.String, nullable=True)
    student_cv_link = db.Column(db.String, nullable=True)
    languages_fluency = db.Column(db.String, nullable=False)
    
    tags = db.Column(db.String, nullable=True)
    jaq = db.Column(db.String, nullable=False, default='JAQ5')
    school_master_name = db.Column(db.String, nullable=True)
    
    is_employed = db.Column(db.Boolean, nullable=False, default=False)
    
    csa_hs_id = db.Column(db.String, db.ForeignKey('career_success_advisors.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    

