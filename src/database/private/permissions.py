from src.database.database_basis import db


class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, nullable=False)
    campaigns = db.Column(db.Integer, nullable=False)
    adgroups = db.Column(db.Integer, nullable=False)
    ads = db.Column(db.Integer, nullable=False)
    reports = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Integer)
