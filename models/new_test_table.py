from db import db
from uuid import uuid4


class NewTestTableModel(db.Model):
    __tablename__ = 'new_test_table'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    some_string = db.Column(db.String, nullable=True)
    some_float = db.Column(db.Float, default=0.0)
    some_integer = db.Column(db.Integer, default=0)