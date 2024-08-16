from db import db


class IntercomReportConversations(db.Model):
    __tablename__ = 'intercom_report_conversations'

    type = db.Column(db.String)
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
    waiting_since = db.Column(db.Integer)
    snoozed_until = db.Column(db.String)
    source = db.Column(db.JSON)
    contacts = db.Column(db.JSON)
    first_contact_reply = db.Column(db.JSON)
    admin_assignee_id = db.Column(db.Integer)
    team_assignee_id = db.Column(db.String)
    open = db.Column(db.Boolean)
    state = db.Column(db.String)
    read = db.Column(db.Boolean)
    tags = db.Column(db.JSON)
    priority = db.Column(db.String)
    sla_applied = db.Column(db.String)
    statistics = db.Column(db.JSON)
    conversation_rating = db.Column(db.JSON)
    teammates = db.Column(db.JSON)
    title = db.Column(db.String)
    custom_attributes = db.Column(db.JSON)
    topics = db.Column(db.JSON)
    conversation_parts = db.Column(db.JSON)
