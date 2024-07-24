from db import db
from uuid import uuid4


class StudentNewPaymentModel(db.Model):
	__tablename__ = 'student_new_payment'

	id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
	hubspot_id = db.Column(db.String, nullable=False, unique=True)
	student_id = db.Column(db.String, nullable=True)
	type_of_collection = db.Column(db.String, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())