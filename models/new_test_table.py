from db import db
from uuid import uuid4


class NewTestTableModel(db.Model):
    __tablename__ = 'new_test_table'
    
    hubspot_id = db.Column(db.String, primary_key=True)
    type_of_collection_code = db.Column(db.String)
    created_at = db.Column(db.String)
    amount = db.Column(db.String)
