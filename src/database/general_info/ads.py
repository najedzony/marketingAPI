from src.database.database_basis import db


class Ads(db.Model):
    advertiser_id = db.Column(db.Integer, nullable=False)
    campaign_id = db.Column(db.Integer, nullable=False)
    adgroup_id = db.Column(db.Integer, nullable=False)
    ad_id = db.Column(db.Integer, primary_key=True)
    ad_name = db.Column(db.String, unique=True, nullable=False)
    creation_date = db.Column(db.DateTime)
    last_update_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"Ad {self.adgroup_name}"
