from db import db
from uuid import uuid4


class CareerSuccessAdvisor(db.Model):
    __tablename__ = 'career_success_advisors'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    csa_fullname = db.Column(db.String, nullable=False)
    csa_email = db.Column(db.String, nullable=False)
    

