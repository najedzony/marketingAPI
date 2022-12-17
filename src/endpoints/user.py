import http

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.database.private.user import Users

user = Blueprint("user", __name__, url_prefix="/api/v1/user")


@user.get("/info")
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify({"advertiser_id": user.advertiser_id}), http.HTTPStatus.OK
    return jsonify({"error": "No such user."}), http.HTTPStatus.BAD_REQUEST
