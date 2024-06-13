from db import db
from uuid import uuid4


class StudentToJobApplication(db.Model):
    __tablename__ = 'student_applications'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    job_id = db.Column(db.String, nullable=False, unique=False)
    student_id = db.Column(db.String, nullable=False, unique=False)
    job_published_timestamp = db.Column(db.DateTime, nullable=False)
    job_offered_to_student_timestamp = db.Column(db.DateTime)
    student_applied = db.Column(db.Boolean, nullable=True)
    student_response_timestamp = db.Column(db.DateTime, nullable=True)
    no_apply_reason = db.Column(db.String, nullable=True)
    student_location_search = db.Column(db.String, nullable=True)
    source = db.Column(db.String, nullable=False)
