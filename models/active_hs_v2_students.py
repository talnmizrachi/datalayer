from db import db


class ActiveCTStudentsTal1(db.Model):
    __tablename__ = 'active-c-t-students-tal-1'

    Program = db.Column(db.Text)
    Cohort_Date = db.Column(db.Text)
    Contact_ID = db.Column(db.Text, primary_key=True)
    Enrollment_ID = db.Column(db.Text)
