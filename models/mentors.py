from db import db
from uuid import uuid4


class MentorModel(db.Model):
    __tablename__ = 'mentors'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    domain = db.Column(db.String, nullable=False)
    mentor_fullname = db.Column(db.String, nullable=False)
    mentor_email = db.Column(db.String, nullable=False)
    mentor_languages = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    test = db.Column(db.String, nullable=True)


