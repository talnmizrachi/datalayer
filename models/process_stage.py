from db import db
from uuid import uuid4


class StageModel(db.Model):
    __tablename__ = 'process_stage'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4().hex))
    hubspot_deal_id = db.Column(db.String, nullable=True)
    process_id = db.Column(db.String, db.ForeignKey('processes.id'), nullable=False)
    stage_in_funnel = db.Column(db.String, nullable=False)
    type_of_stage = db.Column(db.String, nullable=True)
    is_pass = db.Column(db.String, nullable=False, default="PENDING")
    stage_date = db.Column(db.Date, nullable=False)
    deal_stage = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __str__(self):
        return f"Process Stage {self.stage_in_funnel}, {self.type_of_stage} marked as {self.is_pass}"