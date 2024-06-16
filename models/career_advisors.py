from db import db
from uuid import uuid4


class CareerSuccessAdvisorModel(db.Model):
    __tablename__ = 'career_success_advisors'
    
    csa_fullname = db.Column(db.String, nullable=False, primary_key=True)
    csa_email = db.Column(db.String, nullable=False)
    

