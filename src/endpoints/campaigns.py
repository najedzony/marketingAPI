import http
from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants.permissions import WRITE_ACCESS, READ_ACCESS, ADMIN_ACCESS
from src.database.general_info.ads import Ads
from src.database.database_basis import db
from src.database.general_info.adgroups import Adgroups
from src.database.general_info.campaigns import Campaigns
from src.services.useful_funcs import EndpointManagingHelper
from src.services.validator import Validator

campaigns = Blueprint("campaigns", __name__, url_prefix="/api/v1/campaign")
validator = Validator()
helper = EndpointManagingHelper()


@campaigns.post("/add")
@jwt_required()
def add_campaign():
    schema = (
        ("campaign_name", "STRING", True),
        ("total_budget", "INTEGER", False),
        ("daily_budget", "INTEGER", False),
        ("status", "STRING", True),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    unique_fields = ("campaign_name",)
    parameters = (
        "campaign_name",
        "total_budget",
        "daily_budget",
        "status",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_unique(unique_fields, request.json, Campaigns)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    user = helper.get_user(get_jwt_identity())

    if not helper.check_user_permissions(user.advertiser_id, WRITE_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaign = Campaigns(
        advertiser_id=user.advertiser_id,
        campaign_name=request.json["campaign_name"],
        total_budget=request.json.get("total_budget", 0),
        daily_budget=request.json.get("daily_budget", 0),
        creation_date=datetime.utcnow(),
        status=request.json["status"],
    )
    db.session.add(campaign)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Campaign created",
                "campaign": {
                    "campaign_id": campaign.campaign_id,
                    "campaign_name": campaign.campaign_name,
                },
            }
        ),
        http.HTTPStatus.CREATED,
    )


@campaigns.get("/get")
@jwt_required()
def get_campaign():
    schema = (("campaign_id", "INTEGER", True),)
    params = ("campaign_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(params, request.json)
    except Exception as error:
        return jsonify({"error": error}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaign = Campaigns.query.filter_by(
        campaign_id=request.json["campaign_id"], advertiser_id=advertiser_id
    ).first()
    if campaign:
        return (
            jsonify(
                {
                    "campaign_id": campaign.campaign_id,
                    "campaign_name": campaign.campaign_name,
                    "total_budget": campaign.total_budget,
                    "daily_budget": campaign.daily_budget,
                    "creation_date": campaign.creation_date,
                    "last_update_date": campaign.last_update_date,
                    "deletion_date": campaign.deletion_date,
                    "status": campaign.status,
                }
            ),
            http.HTTPStatus.OK,
        )
    else:
        return (
            jsonify(
                {
                    "error": f"There's no campaign with campaign_id {request.json['campaign_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )


@campaigns.get("/list")
@jwt_required()
def get_all_campaigns():
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, READ_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaigns = Campaigns.query.filter_by(advertiser_id=advertiser_id)
    if campaigns.first():
        return (
            jsonify(
                [
                    {
                        "campaign_id": campaign.campaign_id,
                        "campaign_name": campaign.campaign_name,
                        "total_budget": campaign.total_budget,
                        "daily_budget": campaign.daily_budget,
                        "creation_date": campaign.creation_date,
                        "last_update_date": campaign.last_update_date,
                        "deletion_date": campaign.deletion_date,
                        "status": campaign.status,
                    }
                    for campaign in campaigns
                    if campaign.status != "DELETED"
                ]
            ),
            http.HTTPStatus.OK,
        )
    return jsonify(
        {"error": f"There are no campaigns for advertiser if {advertiser_id}."}
    )


@campaigns.post("/update")
@jwt_required()
def update_campaign():
    schema = (
        ("campaign_id", "INTEGER", True),
        ("total_budget", "INTEGER", False),
        ("daily_budget", "INTEGER", False),
        ("status", "STRING", False),
    )
    enum_values = (("status", ("ENABLED", "DISABLED")),)
    parameters = (
        "campaign_id",
        "total_budget",
        "daily_budget",
        "status",
    )
    immutable = ("campaign_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, WRITE_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaign = Campaigns.query.filter_by(
        campaign_id=request.json["campaign_id"], advertiser_id=advertiser_id
    ).first()
    if not campaign:
        return (
            jsonify(
                {
                    "error": f"There's no campaign with campaign_id {request.json['campaign_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    if campaign.status == "DELETED":
        return jsonify(
            {"error": f"Campaign with {request.json['campaign_id']} id was deleted."}
        )
    for parameter in request.json:
        if parameter not in immutable:
            setattr(campaign, parameter, request.json[parameter])
    campaign.last_update_date = datetime.utcnow()
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Campaign updated",
                "campaign": {
                    "campaign_id": campaign.campaign_id,
                    "campaign_name": campaign.campaign_name,
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


def delete_adgroups(campaign_id):
    adgroups = Adgroups.query.filter_by(campaign_id=campaign_id)
    for adgroup in adgroups:
        adgroup.status = "DELETED"
        if not adgroup.deletion_date:
            adgroup.deletion_date = datetime.utcnow()
        delete_ads(adgroup.adgroup_id)
    db.session.commit()


@campaigns.post("/delete")
@jwt_required()
def delete_campaign():
    schema = (("campaign_id", "INTEGER", True),)
    parameters = ("campaign_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaign = Campaigns.query.filter_by(
        campaign_id=request.json["campaign_id"], advertiser_id=advertiser_id
    ).first()
    if not campaign:
        return (
            jsonify(
                {
                    "error": f"There's no campaign with campaign_id {request.json['campaign_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    campaign.deletion_date = datetime.utcnow()
    campaign.status = "DELETED"
    helper.lazy_delete(Campaigns)
    delete_adgroups(request.json["campaign_id"])
    return (
        jsonify(
            {
                "message": "Campaign deleted",
                "campaign": {"campaign_id": campaign.campaign_id},
            }
        ),
        http.HTTPStatus.OK,
    )


@campaigns.post("/undelete")
@jwt_required()
def undelete_campaign():
    schema = (("campaign_id", "INTEGER", True),)
    parameters = ("campaign_id",)
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADMIN_ACCESS, "campaigns"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    campaign = Campaigns.query.filter_by(
        advertiser_id=advertiser_id,
        campaign_id=request.json["campaign_id"],
        status="DELETED",
    ).first()
    if not campaign:
        return (
            jsonify(
                {
                    "error": f"There's no deleted campaign with id {request.json['campaign_id']}"
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
    campaign.deletion_date = None
    campaign.status = "ENABLED"
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Campaign undeleted",
                "campaign": {"campaign_id": campaign.campaign_id},
            }
        ),
        http.HTTPStatus.OK,
    )
