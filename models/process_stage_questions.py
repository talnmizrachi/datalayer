from db import db
from uuid import uuid4


class RealQuestion(db.Model):
    __tablename__ = 'asked_questions'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    stage_id = db.Column(db.String, db.ForeignKey('process_stage.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=True)
    date_asked = db.Column(db.DateTime, default=db.func.current_timestamp())
    