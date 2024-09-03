from uuid import uuid4
from db import db
from sqlalchemy.dialects.postgresql import JSON


class JobReadyStudentsLegacy(db.Model):
    __tablename__ = "static_v3_students"

    token = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    form_id = db.Column(db.String, nullable=True, unique=False)
    submission_date = db.Column(db.DateTime, nullable=False, unique=False)
    domain = db.Column(db.String, nullable=False, unique=False)

    student_first_name = db.Column(db.String, nullable=False, unique=False)
    student_last_name = db.Column(db.String, nullable=False, unique=False)
    best_contact_method = db.Column(db.String, nullable=False, unique=False)

    slack_id = db.Column(db.String, nullable=True, unique=True)
    email_address = db.Column(db.String, nullable=False, unique=False)
    phone_number = db.Column(db.String, nullable=True, unique=False)

    country = db.Column(db.String, nullable=False, unique=False)
    state = db.Column(db.String, nullable=True, unique=False)
    city = db.Column(db.String, nullable=False, unique=False)

    linkedin_url = db.Column(db.String, nullable=False, unique=False)
    resume_url = db.Column(db.String, nullable=False, unique=False)
    cover_letter_url = db.Column(db.String, nullable=True, unique=False)

    preference_company_size = db.Column(db.String, nullable=False, unique=False)
    preference_sectors = db.Column(db.String, nullable=False, unique=False)
    preference_location = db.Column(db.String, nullable=False, unique=False)
    employment_state = db.Column(db.String, nullable=False, unique=False)
    past_employment = db.Column(db.String, nullable=False, unique=False)
    motivation = db.Column(db.String, nullable=False, unique=False)
    goals = db.Column(db.String, nullable=True, unique=False)
    other_projects = db.Column(db.Boolean, nullable=False, unique=False)
    other_projects_text = db.Column(db.String, nullable=True, unique=False)
    onboarding_link = db.Column(db.String, nullable=True, unique=False)
    locations_json = db.Column(db.String, nullable=True, unique=False)

    is_working = db.Column(db.Integer, nullable=True, unique=False)
    email_notification = db.Column(db.Boolean, nullable=True, unique=False)

    subproject = db.Column(db.String, nullable=True, unique=False)

    enable_not_junior = db.Column(db.Boolean, nullable=True)

    languages = db.Column(JSON, nullable=True, unique=False)
    past_experiences = db.Column(JSON, nullable=True, unique=False)
    education = db.Column(JSON, nullable=True, unique=False)
    skills = db.Column(JSON, nullable=True, unique=False)

    diversity_is_black = db.Column(db.Boolean, nullable=True, unique=False)
    diversity_is_woman = db.Column(db.Boolean, nullable=True, unique=False)
    diversity_is_latin = db.Column(db.Boolean, nullable=True, unique=False)

    record_id = db.Column(db.String, nullable=True, unique=True)
    opened_a_deal = db.Column(db.Boolean, nullable=True, unique=False)