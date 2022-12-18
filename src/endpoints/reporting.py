import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from src.constants.permissions import (
    ADVERTISER_REPORTS,
    CAMPAIGNS_REPORTS,
    ADGROUPS_REPORTS,
    ADS_REPORTS,
)
from src.database.database_basis import db
from src.database.reporting.ads import AdsReports
from src.database.reporting.adgroups import AdgroupsReports
from src.database.reporting.advertiser import AdvertiserReports
from src.database.reporting.campaigns import CampaignsReports
from src.services.useful_funcs import EndpointManagingHelper
from src.services.validator import Validator

reports = Blueprint("reports", __name__, url_prefix="/api/v1/reports")
validator = Validator()
helper = EndpointManagingHelper()


@reports.get("/advertiser")
@jwt_required()
def advertiser_reports():
    schema = (
        ("date_from", "STRING", True),
        ("date_to", "STRING", True),
    )
    parameters = (
        "date_from",
        "date_to",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADVERTISER_REPORTS, "reports"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    date_from = helper.create_date_from_string(request.json["date_from"])
    date_to = helper.create_date_from_string(request.json["date_to"])
    reports = AdvertiserReports.query.filter(
        AdvertiserReports.advertiser_id == advertiser_id,
        AdvertiserReports.report_date <= date_to,
        AdvertiserReports.report_date >= date_from,
    )
    if reports.first():
        return (
            jsonify(
                [
                    {
                        "advertiser_id": report.advertiser_id,
                        "report_date": report.report_date,
                        "impressions": report.impressions,
                        "clicks": report.clicks,
                        "cost_per_click": report.cost_per_click,
                        "spend": report.spend,
                        "downloads": report.downloads,
                        "cost_per_download": report.cost_per_download,
                        "installs": report.installs,
                        "cost_per_install": report.cost_per_install,
                    }
                    for report in reports
                ]
            ),
            http.HTTPStatus.OK,
        )
    else:
        return jsonify([]), http.HTTPStatus.OK


@reports.get("/campaigns")
@jwt_required()
def campaigns_reports():
    schema = (
        ("date_from", "STRING", True),
        ("date_to", "STRING", True),
        ("group_by", "STRING", False),
    )
    enum_values = (("group_by", ("CAMPAIGN_ID", "REPORT_DATE")),)
    parameters = (
        "date_from",
        "date_to",
        "group_by",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, CAMPAIGNS_REPORTS, "reports"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    date_from = helper.create_date_from_string(request.json["date_from"])
    date_to = helper.create_date_from_string(request.json["date_to"])
    if "group_by" in request.json:
        if request.json["group_by"].lower() == "campaign_id":
            reports = (
                db.session.query(
                    CampaignsReports.campaign_id,
                    CampaignsReports.campaign_name,
                    func.sum(CampaignsReports.impressions).label("impressions"),
                    func.sum(CampaignsReports.clicks).label("clicks"),
                    func.sum(CampaignsReports.spend).label("spend"),
                    func.sum(CampaignsReports.downloads).label("downloads"),
                    func.sum(CampaignsReports.installs).label("installs"),
                )
                .group_by(CampaignsReports.campaign_id, CampaignsReports.campaign_name)
                .filter(CampaignsReports.report_date >= request.json["date_from"], CampaignsReports.report_date <= request.json["date_to"])
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "campaign_id": report.campaign_id,
                            "campaign_name": report.campaign_name,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
        if request.json["group_by"].lower() == "report_date":
            reports = (
                db.session.query(
                    CampaignsReports.report_date,
                    func.sum(CampaignsReports.impressions).label("impressions"),
                    func.sum(CampaignsReports.clicks).label("clicks"),
                    func.sum(CampaignsReports.spend).label("spend"),
                    func.sum(CampaignsReports.downloads).label("downloads"),
                    func.sum(CampaignsReports.installs).label("installs"),
                )
                .group_by(CampaignsReports.report_date)
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "report_date": report.report_date,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
    else:
        reports = CampaignsReports.query.filter(
            CampaignsReports.advertiser_id == advertiser_id,
            CampaignsReports.report_date <= date_to,
            CampaignsReports.report_date >= date_from,
        )
        return (
            jsonify(
                [
                    {
                        "campaign_id": report.campaign_id,
                        "campaign_name": report.campaign_name,
                        "report_date": report.report_date,
                        "impressions": report.impressions,
                        "clicks": report.clicks,
                        "cost_per_click": report.cost_per_click,
                        "spend": report.spend,
                        "downloads": report.downloads,
                        "cost_per_download": report.cost_per_download,
                        "installs": report.installs,
                        "cost_per_install": report.cost_per_install,
                    }
                    for report in reports
                ]
            ),
            http.HTTPStatus.OK,
        )


@reports.get("/adgroups")
@jwt_required()
def adgroups_reports():
    schema = (
        ("date_from", "STRING", True),
        ("date_to", "STRING", True),
        ("group_by", "STRING", False),
    )
    enum_values = (("group_by", ("ADGROUP_ID", "REPORT_DATE")),)
    parameters = (
        "date_from",
        "date_to",
        "group_by",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADGROUPS_REPORTS, "reports"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    date_from = helper.create_date_from_string(request.json["date_from"])
    date_to = helper.create_date_from_string(request.json["date_to"])
    if "group_by" in request.json:
        if request.json["group_by"].lower() == "adgroup_id":
            reports = (
                db.session.query(
                    AdgroupsReports.adgroup_id,
                    AdgroupsReports.adgroup_name,
                    func.sum(AdgroupsReports.impressions).label("impressions"),
                    func.sum(AdgroupsReports.clicks).label("clicks"),
                    func.sum(AdgroupsReports.spend).label("spend"),
                    func.sum(AdgroupsReports.downloads).label("downloads"),
                    func.sum(AdgroupsReports.installs).label("installs"),
                )
                .group_by(AdgroupsReports.adgroup_id, AdgroupsReports.adgroup_name)
                .filter(AdgroupsReports.report_date >= request.json["date_from"],
                        AdgroupsReports.report_date <= request.json["date_to"])
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "adgroup_id": report.adgroup_id,
                            "adgroup_name": report.adgroup_name,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
        if request.json["group_by"].lower() == "report_date":
            reports = (
                db.session.query(
                    AdgroupsReports.report_date,
                    func.sum(AdgroupsReports.impressions).label("impressions"),
                    func.sum(AdgroupsReports.clicks).label("clicks"),
                    func.sum(AdgroupsReports.spend).label("spend"),
                    func.sum(AdgroupsReports.downloads).label("downloads"),
                    func.sum(AdgroupsReports.installs).label("installs"),
                )
                .group_by(AdgroupsReports.report_date)
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "report_date": report.report_date,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
    else:
        reports = AdgroupsReports.query.filter(
            AdgroupsReports.advertiser_id == advertiser_id,
            AdgroupsReports.report_date <= date_to,
            AdgroupsReports.report_date >= date_from,
        )
        return (
            jsonify(
                [
                    {
                        "campaign_id": report.campaign_id,
                        "adgroup_id": report.adgroup_id,
                        "adgroup_name": report.adgroup_name,
                        "report_date": report.report_date,
                        "impressions": report.impressions,
                        "clicks": report.clicks,
                        "cost_per_click": report.cost_per_click,
                        "spend": report.spend,
                        "downloads": report.downloads,
                        "cost_per_download": report.cost_per_download,
                        "installs": report.installs,
                        "cost_per_install": report.cost_per_install,
                    }
                    for report in reports
                ]
            ),
            http.HTTPStatus.OK,
        )


@reports.get("/ads")
@jwt_required()
def ads_reports():
    schema = (
        ("date_from", "STRING", True),
        ("date_to", "STRING", True),
        ("group_by", "STRING", False),
    )
    enum_values = (("group_by", ("AD_ID", "REPORT_DATE")),)
    parameters = (
        "date_from",
        "date_to",
        "group_by",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_values(enum_values, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_user_permissions(advertiser_id, ADS_REPORTS, "reports"):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    date_from = helper.create_date_from_string(request.json["date_from"])
    date_to = helper.create_date_from_string(request.json["date_to"])
    if "group_by" in request.json:
        if request.json["group_by"].lower() == "ad_id":
            reports = (
                db.session.query(
                    AdsReports.ad_id,
                    AdsReports.ad_name,
                    func.sum(AdsReports.impressions).label("impressions"),
                    func.sum(AdsReports.clicks).label("clicks"),
                    func.sum(AdsReports.spend).label("spend"),
                    func.sum(AdsReports.downloads).label("downloads"),
                    func.sum(AdsReports.installs).label("installs"),
                )
                .group_by(AdsReports.ad_id, AdsReports.ad_name)
                .filter(AdsReports.report_date >= request.json["date_from"],
                        AdsReports.report_date <= request.json["date_to"])
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "ad_id": report.ad_id,
                            "ad_name": report.ad_name,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
        if request.json["group_by"].lower() == "report_date":
            reports = (
                db.session.query(
                    AdsReports.report_date,
                    func.sum(AdsReports.impressions).label("impressions"),
                    func.sum(AdsReports.clicks).label("clicks"),
                    func.sum(AdsReports.spend).label("spend"),
                    func.sum(AdsReports.downloads).label("downloads"),
                    func.sum(AdsReports.installs).label("installs"),
                )
                .group_by(AdsReports.report_date)
                .all()
            )
            return (
                jsonify(
                    [
                        {
                            "report_date": report.report_date,
                            "impressions": report.impressions,
                            "clicks": report.clicks,
                            "cost_per_click": report.spend / report.clicks,
                            "spend": report.spend,
                            "downloads": report.downloads,
                            "cost_per_download": report.spend / report.downloads,
                            "installs": report.installs,
                            "cost_per_install": report.spend / report.installs,
                        }
                        for report in reports
                    ]
                ),
                http.HTTPStatus.OK,
            )
    else:
        reports = AdsReports.query.filter(
            AdsReports.advertiser_id == advertiser_id,
            AdsReports.report_date <= date_to,
            AdsReports.report_date >= date_from,
        )
        return (
            jsonify(
                [
                    {
                        "campaign_id": report.campaign_id,
                        "adgroup_id": report.adgroup_id,
                        "ad_id": report.ad_id,
                        "ad_name": report.ad_name,
                        "report_date": report.report_date,
                        "impressions": report.impressions,
                        "clicks": report.clicks,
                        "cost_per_click": report.cost_per_click,
                        "spend": report.spend,
                        "downloads": report.downloads,
                        "cost_per_download": report.cost_per_download,
                        "installs": report.installs,
                        "cost_per_install": report.cost_per_install,
                    }
                    for report in reports
                ]
            ),
            http.HTTPStatus.OK,
        )
