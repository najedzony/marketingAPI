from src.database.database_basis import db


class AdsReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, nullable=False)
    campaign_id = db.Column(db.Integer, nullable=False)
    adgroup_id = db.Column(db.Integer, nullable=False)
    ad_id = db.Column(db.Integer, nullable=False)
    ad_name = db.Column(db.String, nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    cost_per_click = db.Column(db.Float)
    spend = db.Column(db.Float)
    downloads = db.Column(db.Integer)
    cost_per_download = db.Column(db.Float)
    installs = db.Column(db.Integer)
    cost_per_install = db.Column(db.Float)
