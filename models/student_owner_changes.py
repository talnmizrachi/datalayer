from db import db
from uuid import uuid4


class StudentOwnerChangesModel(db.Model):
    __tablename__ = 'student_owner_changes'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    student_hubspot_id = db.Column(db.String, nullable=False)
    student_hubspot_owner_id = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


