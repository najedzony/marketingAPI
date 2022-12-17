import os

from flask import Flask
from flask_jwt_extended import JWTManager

from src.database.database_basis import db
from src.endpoints.adgroups import adgroups
from src.endpoints.ads import ads
from src.endpoints.auth import auth
from src.endpoints.campaigns import campaigns
from src.endpoints.reporting import reports
from src.endpoints.uploading_reports import uploading_reports
from src.endpoints.user import user

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
)


app.register_blueprint(auth)
app.register_blueprint(campaigns)
app.register_blueprint(user)
app.register_blueprint(adgroups)
app.register_blueprint(ads)
app.register_blueprint(reports)
app.register_blueprint(uploading_reports)

JWTManager(app)
db.init_app(app)
