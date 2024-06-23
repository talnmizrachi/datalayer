from db import db
from uuid import uuid4


class StudentStagesV3(db.Model):
    __tablename__ = 'student_deal_stages'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    student_id = db.Column(db.String, nullable=False)
    hubspot_id = db.Column(db.String, nullable=False)
    stage = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    

