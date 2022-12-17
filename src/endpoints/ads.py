import http
from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants.permissions import WRITE_ACCESS, READ_ACCESS, ADMIN_ACCESS
from src.database.database_basis import db
from src.database.general_info.adgroups import Adgroups
from src.database.general_info.ads import Ads
from src.services.useful_funcs import EndpointManagingHelper
from src.services.validator import Validator

ads = Blueprint("ads", __name__, url_prefix="/api/v1/ads")
validator = Validator()
helper = EndpointManagingHelper()


@ads.post("/add")
@jwt_required()
def add_ad():
    schema = (
        ("adgroup_id", "INTEGER", True),
        ("ad_name", "STRING", True),
        ("status", "STRING", True),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    unique_fields = ("ad_name",)
    parameters = (
        "adgroup_id",
        "ad_name",
        "status",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_unique(unique_fields, request.json, Ads)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, WRITE_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    check_adgroup_exists = Adgroups.query.filter_by(
        advertiser_id=advertiser_id, adgroup_id=request.json["adgroup_id"]
    )
    if (
        check_adgroup_exists.first()
        and check_adgroup_exists.first().status != "DELETED"
    ):
        campaign_id = check_adgroup_exists.first().campaign_id
        ad = Ads(
            advertiser_id=advertiser_id,
            campaign_id=campaign_id,
            adgroup_id=request.json["adgroup_id"],
            ad_name=request.json["ad_name"],
            creation_date=datetime.utcnow(),
            status=request.json["status"],
        )
        db.session.add(ad)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Ad created",
                    "adgroup": {
                        "ad_id": ad.ad_id,
                        "ad_name": ad.ad_name,
                        "adgroup_id": ad.adgroup_id,
                        "campaign_id": ad.campaign_id,
                    },
                }
            ),
            http.HTTPStatus.CREATED,
        )
    return (
        jsonify({"error": f"There's no adgroup id {request.json['adgroup_id']}."}),
        http.HTTPStatus.BAD_REQUEST,
    )


@ads.get("/get")
@jwt_required()
def get_ad():
    schema = (("ad_id", "INTEGER", True),)
    params = ("ad_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(params, request.json)
    except Exception as error:
        return jsonify({"error": error}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ad = Ads.query.filter_by(
        ad_id=request.json["ad_id"], advertiser_id=advertiser_id
    ).first()
    if ad:
        return (
            jsonify(
                {
                    "campaign_id": ad.campaign_id,
                    "adgroup_id": ad.adgroup_id,
                    "ad_id": ad.ad_id,
                    "ad_name": ad.ad_name,
                    "creation_date": ad.creation_date,
                    "last_update_date": ad.last_update_date,
                    "deletion_date": ad.deletion_date,
                    "status": ad.status,
                }
            ),
            http.HTTPStatus.OK,
        )
    return (
        jsonify({"error": f"There's no ad with id {request.json['ad_id']}"}),
        http.HTTPStatus.BAD_REQUEST,
    )


@ads.get("/list")
@jwt_required()
def get_all_ads():
    schema = (("adgroup_id", "INTEGER", True),)
    params = ("adgroup_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(params, request.json)
    except Exception as error:
        return jsonify({"error": error}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ads = Ads.query.filter_by(
        advertiser_id=advertiser_id, adgroup_id=request.json["adgroup_id"]
    )
    if ads.first():
        return (
            jsonify(
                [
                    {
                        "campaign_id": ad.campaign_id,
                        "adgroup_id": ad.adgroup_id,
                        "ad_id": ad.ad_id,
                        "ad_name": ad.ad_name,
                        "creation_date": ad.creation_date,
                        "last_update_date": ad.last_update_date,
                        "deletion_date": ad.deletion_date,
                        "status": ad.status,
                    }
                    for ad in ads
                ]
            ),
            http.HTTPStatus.OK,
        )
    return jsonify(
        {"error": f"There are no ads for adgroup id {request.json['adgroup_id']}"}
    )


@ads.post("/update")
@jwt_required()
def update_ad():
    schema = (
        ("ad_id", "INTEGER", True),
        ("status", "STRING", False),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    parameters = (
        "ad_id",
        "status",
    )
    immutable = ("ad_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, WRITE_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ad = Ads.query.filter_by(
        ad_id=request.json["ad_id"], advertiser_id=advertiser_id
    ).first()
    if not ad:
        return (
            jsonify({"error": f"There's no ad with ad id {request.json['ad_id']}."}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if ad.status == "DELETED":
        return jsonify({"error": f"Ad with {request.json['ad_id']} id was deleted."})
    for parameter in request.json:
        if parameter not in immutable:
            setattr(ad, parameter, request.json[parameter])
    ad.last_update_date = datetime.utcnow()
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Ad updated",
                "ad": {
                    "ad_id": ad.ad_id,
                    "ad_name": ad.ad_name,
                },
            }
        ),
        http.HTTPStatus.OK,
    )


@ads.post("/delete")
@jwt_required()
def delete_ad():
    schema = (("ad_id", "INTEGER", True),)
    parameters = ("ad_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ad = Ads.query.filter_by(
        ad_id=request.json["ad_id"], advertiser_id=advertiser_id
    ).first()
    if not ad:
        return (
            jsonify({"error": f"There's no ad with ad id {request.json['ad_id']}."}),
            http.HTTPStatus.BAD_REQUEST,
        )
    ad.deletion_date = datetime.utcnow()
    ad.status = "DELETED"
    helper.lazy_delete(Ads)
    return (
        jsonify(
            {
                "message": "Ad deleted",
                "adgroup": {"ad_id": ad.ad_id},
            }
        ),
        http.HTTPStatus.OK,
    )


@ads.post("/undelete")
@jwt_required()
def undelete_ads():
    schema = (("ad_id", "INTEGER", True),)
    parameters = ("ad_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "ads"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ad = Ads.query.filter_by(
        advertiser_id=advertiser_id,
        ad_id=request.json["ad_id"],
        status="DELETED",
    ).first()
    if not ad:
        return (
            jsonify(
                {"error": f"There's no deleted ad with id {request.json['ad_id']}"}
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    adgroup = Adgroups.query.filter_by(
        advertiser_id=advertiser_id, adgroup_id=ad.adgroup_id
    ).first()
    if not adgroup or adgroup.status == "DELETED":
        return (
            jsonify({"error": "Ad's adgroup is deleted."}),
            http.HTTPStatus.BAD_REQUEST,
        )
    ad.deletion_date = None
    ad.status = "ENABLED"
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Ad undeleted",
                "adgroup": {"ad_id": ad.ad_id},
            }
        ),
        http.HTTPStatus.OK,
    )
