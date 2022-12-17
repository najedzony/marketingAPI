import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from src.database.private.permissions import Permissions
from src.database.database_basis import db
from src.database.private.user import Users
from src.services.useful_funcs import EndpointManagingHelper

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
helper = EndpointManagingHelper()


def get_tokens(identity):
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


"""
Max permissions:
{
    "campaigns": ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"],
    "adgroups": ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"],
    "ads": ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"],
    "reports": [
        "ADVERTISER_REPORTS",
        "CAMPAIGNS_REPORTS",
        "ADGROUPS_REPORTS",
        "ADS_REPORTS",
        "UPLOAD_REPORTS"
    ]
}
"""


def set_permissions(request, user):
    campaigns_permissions = 0
    if "campaigns" in request.json["permissions"]:
        campaigns_permissions = helper.update_permissions(
            request.json["permissions"], "campaigns"
        )
    adgroups_permissions = 0
    if "adgroups" in request.json["permissions"]:
        adgroups_permissions = helper.update_permissions(
            request.json["permissions"], "adgroups"
        )
    ads_permissions = 0
    if "ads" in request.json["permissions"]:
        ads_permissions = helper.update_permissions(request.json["permissions"], "ads")
    reports_permissions = 0
    if "reports" in request.json["permissions"]:
        reports_permissions = helper.update_reports_permissions(
            request.json["permissions"]
        )
    permissions = Permissions(
        advertiser_id=user.advertiser_id,
        campaings=campaigns_permissions,
        adgroups=adgroups_permissions,
        ads=ads_permissions,
        reports=reports_permissions,
    )
    db.session.add(permissions)


@auth.post("/register")
def register():
    username = request.json["username"]
    password = request.json["password"]

    if len(password) < 10:
        return (
            jsonify(
                {"error": "Password is too short"},
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    hashed_password = generate_password_hash(password)
    advertiser_id = db.session.query(func.max(Users.advertiser_id)).first()[0] + 1
    user = Users(
        username=username,
        password=hashed_password,
        advertiser_id=advertiser_id,
    )
    db.session.add(user)
    set_permissions(request, user)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "User created",
                "user": {
                    "username": username,
                    "advertiser_id": advertiser_id,
                },
            }
        ),
        http.HTTPStatus.CREATED,
    )


@auth.post("/authenticate")
def authenticate():
    username = request.json["username"]
    password = request.json["password"]

    user = Users.query.filter_by(username=username).first()

    if user:
        is_password_correct = check_password_hash(user.password, password)
        if is_password_correct:
            access_token, refresh_token = get_tokens(user.user_id)
            return (
                jsonify(
                    {
                        "user": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                        }
                    }
                ),
                http.HTTPStatus.ACCEPTED,
            )

    return jsonify({"error": "Wrong credentials"}), http.HTTPStatus.UNAUTHORIZED


@auth.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), http.HTTPStatus.OK
