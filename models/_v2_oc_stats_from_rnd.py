from db import db


class V2OcStatsFromRnd(db.Model):
    __tablename__ = '_v2_oc_stats_from_rnd'

    start_date = db.Column(db.Date, primary_key=True)
    n_students = db.Column(db.Integer)
    n_converted = db.Column(db.Integer)
    conversion_rate = db.Column(db.Float)

    __table_args__ = {'schema': 'public'}
