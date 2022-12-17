from src.database.database_basis import db


class Adgroups(db.Model):
    advertiser_id = db.Column(db.Integer, nullable=False)
    campaign_id = db.Column(db.Integer, nullable=False)
    adgroup_id = db.Column(db.Integer, primary_key=True)
    adgroup_name = db.Column(db.String, unique=True, nullable=False)
    total_budget = db.Column(db.Integer)
    daily_budget = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    last_update_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"Adgroup {self.adgroup_name}"
