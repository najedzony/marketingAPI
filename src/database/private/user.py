from src.database.database_basis import db


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    advertiser_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User {self.username}"
