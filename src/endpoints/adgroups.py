import http
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants.permissions import WRITE_ACCESS, READ_ACCESS, ADMIN_ACCESS
from src.database.general_info.ads import Ads
from src.database.database_basis import db
from src.database.general_info.adgroups import Adgroups
from src.database.general_info.campaigns import Campaigns
from src.services.useful_funcs import EndpointManagingHelper
from src.services.validator import Validator

adgroups = Blueprint("adgroups", __name__, url_prefix="/api/v1/adgroups")
validator = Validator()
helper = EndpointManagingHelper()


@adgroups.post("/add")
@jwt_required()
def add_adgroup():
    schema = (
        ("campaign_id", "INTEGER", True),
        ("adgroup_name", "STRING", True),
        ("total_budget", "INTEGER", False),
        ("daily_budget", "INTEGER", False),
        ("status", "STRING", True),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    unique_fields = ("adgroup_name",)
    parameters = (
        "adgroup_name",
        "campaign_id",
        "total_budget",
        "daily_budget",
        "status",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_unique(unique_fields, request.json, Adgroups)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST

    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id
    check_campaign_exists = Campaigns.query.filter_by(
        advertiser_id=advertiser_id, campaign_id=request.json["campaign_id"]
    )

    if not helper.check_user_permissions(advertiser_id, WRITE_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    if check_campaign_exists and check_campaign_exists.first().status != "DELETED":
        adgroup = Adgroups(
            advertiser_id=advertiser_id,
            campaign_id=request.json["campaign_id"],
            adgroup_name=request.json["adgroup_name"],
            total_budget=request.json.get("total_budget", 0),
            daily_budget=request.json.get("daily_budget", 0),
            creation_date=datetime.utcnow(),
            status=request.json["status"],
        )
        db.session.add(adgroup)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Adgroup created",
                    "adgroup": {
                        "adgroup_id": adgroup.adgroup_id,
                        "adgroup_name": adgroup.adgroup_name,
                        "campaign_id": adgroup.campaign_id,
                    },
                }
            ),
            http.HTTPStatus.CREATED,
        )
    return (
        jsonify({"error": f"There's no campaign id {request.json['campaign_id']}."}),
        http.HTTPStatus.BAD_REQUEST,
    )


@adgroups.get("/get")
@jwt_required()
def get_adgroup():
    schema = (("adgroup_id", "INTEGER", True),)
    params = ("adgroup_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(params, request.json)
    except Exception as error:
        return jsonify({"error": error}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    adgroup = Adgroups.query.filter_by(
        adgroup_id=request.json["adgroup_id"], advertiser_id=advertiser_id
    ).first()
    if adgroup:
        return (
            jsonify(
                {
                    "campaign_id": adgroup.campaign_id,
                    "adgroup_id": adgroup.adgroup_id,
                    "adgroup_name": adgroup.adgroup_name,
                    "total_budget": adgroup.total_budget,
                    "daily_budget": adgroup.daily_budget,
                    "creation_date": adgroup.creation_date,
                    "last_update_date": adgroup.last_update_date,
                    "deletion_date": adgroup.deletion_date,
                    "status": adgroup.status,
                }
            ),
            http.HTTPStatus.OK,
        )
    else:
        return (
            jsonify(
                {"error": f"There's no adgroup with id {request.json['adgroup_id']}"}
            ),
            http.HTTPStatus.BAD_REQUEST,
        )


@adgroups.get("/list")
@jwt_required()
def get_all_adgroups():
    schema = (("campaign_id", "INTEGER", True),)
    params = ("campaign_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(params, request.json)
    except Exception as error:
        return jsonify({"error": error}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    adgroups = Adgroups.query.filter_by(
        advertiser_id=advertiser_id, campaign_id=request.json["campaign_id"]
    )
    if adgroups.first():
        return (
            jsonify(
                [
                    {
                        "campaign_id": adgroup.campaign_id,
                        "adgroup_id": adgroup.adgroup_id,
                        "adgroup_name": adgroup.adgroup_name,
                        "total_budget": adgroup.total_budget,
                        "daily_budget": adgroup.daily_budget,
                        "creation_date": adgroup.creation_date,
                        "last_update_date": adgroup.last_update_date,
                        "deletion_date": adgroup.deletion_date,
                        "status": adgroup.status,
                    }
                    for adgroup in adgroups
                ]
            ),
            http.HTTPStatus.OK,
        )
    return jsonify(
        {
            "error": f"There are no adgroups for campaign id {request.json['campaign_id']}"
        }
    )


@adgroups.post("/update")
@jwt_required()
def update_adgroup():
    schema = (
        ("adgroup_id", "INTEGER", True),
        ("total_budget", "INTEGER", False),
        ("daily_budget", "INTEGER", False),
        ("status", "STRING", False),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    parameters = (
        "adgroup_id",
        "total_budget",
        "daily_budget",
        "status",
    )
    immutable = ("adgroup_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    adgroup = Adgroups.query.filter_by(
        adgroup_id=request.json["adgroup_id"], advertiser_id=advertiser_id
    ).first()
    if not adgroup:
        return (
            jsonify(
                {
                    "error": f"There's no adgroup with adgroup id {request.json['adgroup_id']}."
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    if adgroup.status == "DELETED":
        return jsonify(
            {"error": f"Adgroup with {request.json['adgroup_id']} id was deleted."}
        )
    for parameter in request.json:
        if parameter not in immutable:
            setattr(adgroup, parameter, request.json[parameter])
    adgroup.last_update_date = datetime.utcnow()
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Adgroup updated",
                "adgroup": {
                    "adgroup_id": adgroup.adgroup_id,
                    "adgroup_name": adgroup.adgroup_name,
                },
            }
        ),
        http.HTTPStatus.OK,
    )


def delete_ads(adgroup_id):
    ads = Ads.query.filter_by(adgroup_id=adgroup_id)
    for ad in ads:
        ad.status = "DELETED"
        if not ad.deletion_date:
            ad.deletion_date = datetime.utcnow()
    db.session.commit()


@adgroups.post("/delete")
@jwt_required()
def delete_adgroup():
    schema = (("adgroup_id", "INTEGER", True),)
    parameters = ("adgroup_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    adgroup = Adgroups.query.filter_by(
        adgroup_id=request.json["adgroup_id"], advertiser_id=advertiser_id
    ).first()
    if not adgroup:
        return (
            jsonify(
                {
                    "error": f"There's no adgroup with adgroup_id {request.json['adgroup_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    adgroup.deletion_date = datetime.utcnow()
    adgroup.status = "DELETED"
    helper.lazy_delete(Adgroups)
    delete_ads(adgroup.adgroup_id)
    return (
        jsonify(
            {
                "message": "Adgroup deleted",
                "adgroup": {"adgroup_id": adgroup.adgroup_id},
            }
        ),
        http.HTTPStatus.OK,
    )


@adgroups.post("/undelete")
@jwt_required()
def undelete_adgroups():
    schema = (("adgroup_id", "INTEGER", True),)
    parameters = "adgroup_id"
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "adgroups"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    adgroup = Adgroups.query.filter_by(
        advertiser_id=advertiser_id,
        adgroup_id=request.json["adgroup_id"],
        status="DELETED",
    ).first()
    if not adgroup:
        return (
            jsonify(
                {
                    "error": f"There's no deleted adgroup with id {request.json['adgroup_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    campaign = Campaigns.query.filter_by(
        advertiser_id=advertiser_id, campaign_id=adgroup.campaign_id
    ).first()
    if not campaign or campaign.status == "DELETED":
        return (
            jsonify({"error": "Adgroup's campaign is deleted."}),
            http.HTTPStatus.BAD_REQUEST,
        )
    adgroup.deletion_date = None
    adgroup.status = "ENABLED"
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Adgroup undeleted",
                "adgroup": {"adgroup_id": adgroup.adgroup_id},
            }
        ),
        http.HTTPStatus.OK,
    )
