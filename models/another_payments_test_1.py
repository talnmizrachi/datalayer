from db import db
from uuid import uuid4


class AnotherNewPayments(db.Model):
    __tablename__ = 'another_payments_test_1'
    
    hubspot_id = db.Column(db.String, primary_key=True)
    type_of_collection_code = db.Column(db.String)
    created_at = db.Column(db.String)
    amount = db.Column(db.String)
