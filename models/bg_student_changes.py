from db import db
from uuid import uuid4


class BGStudentChangesModel(db.Model):
    __tablename__ = 'bg_student_changes'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    hubspot_id = db.Column(db.String, db.ForeignKey('bg_students.hubspot_id'), nullable=False)
    key = db.Column(db.String, nullable=True)
    from_value = db.Column(db.String, nullable=True)
    to_value = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


