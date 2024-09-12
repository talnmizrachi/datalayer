
from db import db


class V3DailyPulseModel(db.Model):
    __tablename__ = "v3_pulse_table"

    date = db.Column(db.String, primary_key=True)
    job_ready_students = db.Column(db.Integer, default=0)
    active_job_searchers = db.Column(db.Integer, default=0)
    daily_applications = db.Column(db.Integer, default=0)
    interview_process_count = db.Column(db.Integer, default=0)
    students_with_interview_process = db.Column(db.Integer, default=0)
    daily_callbacks = db.Column(db.Integer, default=0)
    this_month_callbacks = db.Column(db.Integer, default=0)
    cumulative_monthly_applications = db.Column(db.Integer, default=0)
    cvr_callback_to_applications = db.Column(db.Float, default=0)
    daily_placements = db.Column(db.Integer, default=0)
    monthly_cumulative_placements = db.Column(db.Integer, default=0)
    yearly_cumulative_placements = db.Column(db.Integer, default=0)
    cvr_placement_to_callback = db.Column(db.Float, default=0)
    placement_revenue = db.Column(db.BigInteger, default=0)
    monthly_placements_revenue = db.Column(db.BigInteger, default=0)
    yearly_placements_revenue = db.Column(db.BigInteger, default=0)
    quarterly_cumulative_placements = db.Column(db.Integer, default=0)
    quarterly_placements_revenue = db.Column(db.BigInteger, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

