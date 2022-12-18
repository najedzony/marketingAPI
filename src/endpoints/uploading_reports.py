import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.database.reporting.advertiser import AdvertiserReports
from src.database.general_info.adgroups import Adgroups
from src.database.reporting.adgroups import AdgroupsReports
from src.database.general_info.campaigns import Campaigns
from src.database.reporting.campaigns import CampaignsReports
from src.database.database_basis import db
from src.database.general_info.ads import Ads
from src.database.reporting.ads import AdsReports
from src.services.useful_funcs import EndpointManagingHelper
from src.services.validator import Validator

uploading_reports = Blueprint(
    "upload_reports", __name__, url_prefix="/api/v1/uploadreport"
)
validator = Validator()
helper = EndpointManagingHelper()


@uploading_reports.post("/")
@jwt_required()
def upload_reports():
    schema = (
        ("ad_id", "INTEGER", True),
        ("report_date", "STRING", True),
        ("impressions", "INTEGER", True),
        ("clicks", "INTEGER", True),
        ("spend", "FLOAT", True),
        ("downloads", "INTEGER", True),
        ("installs", "INTEGER", True),
    )
    parameters = (
        "ad_id",
        "installs",
        "report_date",
        "impressions",
        "clicks",
        "spend",
        "downloads",
    )
    try:
        validator.validate_types(schema, request.json)
        validator.validate_names(parameters, request.json)
    except Exception as error:
        return jsonify({"error": error.args}), http.HTTPStatus.BAD_REQUEST
    advertiser_id = helper.get_user(get_jwt_identity()).advertiser_id

    if not helper.check_admin_permissions(advertiser_id):
        return jsonify({"message": "Access denied"}), http.HTTPStatus.UNAUTHORIZED

    ad = Ads.query.filter_by(
        ad_id=request.json["ad_id"]
    ).first()
    if not ad or ad.status == "DELETED":
        return (
            jsonify({"error": f"There's no such ad_id {request.json['ad_id']}"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    ad_report = AdsReports.query.filter(
        AdsReports.advertiser_id == ad.advertiser_id,
        AdsReports.ad_id == ad.ad_id,
        AdsReports.report_date == request.json["report_date"],
    ).first()
    if ad_report:
        for parameter in request.json:
            if parameter != "report_date":
                current_value = getattr(ad_report, parameter)
                setattr(ad_report, parameter, current_value + request.json[parameter])
    else:
        new_report = AdsReports(
            advertiser_id=ad.advertiser_id,
            campaign_id=ad.campaign_id,
            adgroup_id=ad.adgroup_id,
            ad_id=ad.ad_id,
            ad_name=ad.ad_name,
            report_date=request.json["report_date"],
            impressions=request.json["impressions"],
            clicks=request.json["clicks"],
            cost_per_click=request.json["spend"] / request.json["clicks"],
            spend=request.json["spend"],
            downloads=request.json["downloads"],
            cost_per_download=request.json["spend"] / request.json["downloads"],
            installs=request.json["installs"],
            cost_per_install=request.json["spend"] / request.json["installs"],
        )
        db.session.add(new_report)
    add_corresponding_advertiser_report(request.json, ad.advertiser_id)
    add_corresponding_campaign_report(request.json, ad.campaign_id, ad.advertiser_id)
    add_corresponding_adgroup_report(request.json, ad.campaign_id, ad.adgroup_id, ad.advertiser_id)
    db.session.commit()
    return jsonify({"message": "Report added"}), http.HTTPStatus.CREATED


def add_corresponding_campaign_report(request, campaign_id, advertiser_id):
    parameters_to_update = (
        "impressions",
        "clicks",
        "spend",
        "downloads",
        "installs",
    )

    corresponding_campaign_report = CampaignsReports.query.filter(
        CampaignsReports.advertiser_id == advertiser_id,
        CampaignsReports.campaign_id == campaign_id,
        CampaignsReports.report_date == request["report_date"],
    ).first()

    if corresponding_campaign_report:
        for parameter in request:
            if parameter in parameters_to_update:
                current_value = getattr(corresponding_campaign_report, parameter)
                setattr(
                    corresponding_campaign_report,
                    parameter,
                    current_value + request[parameter],
                )
        corresponding_campaign_report.cost_per_clicks = (
            corresponding_campaign_report.spend / corresponding_campaign_report.clicks
        )
        corresponding_campaign_report.cost_per_downloads = (
            corresponding_campaign_report.spend
            / corresponding_campaign_report.downloads
        )
        corresponding_campaign_report.cost_per_installs = (
            corresponding_campaign_report.spend / corresponding_campaign_report.installs
        )

    else:
        campaign_info = Campaigns.query.filter_by(
            advertiser_id=advertiser_id,
            campaign_id=campaign_id,
        ).first()
        new_report = CampaignsReports(
            advertiser_id=advertiser_id,
            campaign_id=campaign_info.campaign_id,
            campaign_name=campaign_info.campaign_name,
            report_date=request["report_date"],
            impressions=request["impressions"],
            clicks=request["clicks"],
            cost_per_click=request["spend"] / request["clicks"],
            spend=request["spend"],
            downloads=request["downloads"],
            cost_per_download=request["spend"] / request["downloads"],
            installs=request["installs"],
            cost_per_install=request["spend"] / request["installs"],
        )
        db.session.add(new_report)


def add_corresponding_adgroup_report(request, campaign_id, adgroup_id, advertiser_id):
    parameters_to_update = (
        "impressions",
        "clicks",
        "spend",
        "downloads",
        "installs",
    )

    corresponding_adgroup_report = AdgroupsReports.query.filter(
        AdgroupsReports.advertiser_id == advertiser_id,
        AdgroupsReports.adgroup_id == adgroup_id,
        AdgroupsReports.report_date == request["report_date"],
    ).first()

    if corresponding_adgroup_report:
        for parameter in request:
            if parameter in parameters_to_update:
                current_value = getattr(corresponding_adgroup_report, parameter)
                setattr(
                    corresponding_adgroup_report,
                    parameter,
                    current_value + request[parameter],
                )
        corresponding_adgroup_report.cost_per_clicks = (
            corresponding_adgroup_report.spend / corresponding_adgroup_report.clicks
        )
        corresponding_adgroup_report.cost_per_downloads = (
            corresponding_adgroup_report.spend / corresponding_adgroup_report.downloads
        )
        corresponding_adgroup_report.cost_per_installs = (
            corresponding_adgroup_report.spend / corresponding_adgroup_report.installs
        )
    else:
        adgroup_info = Adgroups.query.filter_by(
            advertiser_id=advertiser_id, adgroup_id=adgroup_id
        ).first()
        new_report = AdgroupsReports(
            advertiser_id=advertiser_id,
            campaign_id=campaign_id,
            adgroup_id=adgroup_id,
            adgroup_name=adgroup_info.adgroup_name,
            report_date=request["report_date"],
            impressions=request["impressions"],
            clicks=request["clicks"],
            cost_per_click=request["spend"] / request["clicks"],
            spend=request["spend"],
            downloads=request["downloads"],
            cost_per_download=request["spend"] / request["downloads"],
            installs=request["installs"],
            cost_per_install=request["spend"] / request["installs"],
        )
        db.session.add(new_report)


def add_corresponding_advertiser_report(request, advertiser_id):
    parameters_to_update = (
        "impressions",
        "clicks",
        "spend",
        "downloads",
        "installs",
    )
    corresponding_advertiser_report = AdvertiserReports.query.filter(
        AdgroupsReports.advertiser_id == advertiser_id,
        AdgroupsReports.report_date == request["report_date"],
    ).first()
    if corresponding_advertiser_report:
        for parameter in request:
            if parameter in parameters_to_update:
                current_value = getattr(corresponding_advertiser_report, parameter)
                setattr(
                    corresponding_advertiser_report,
                    parameter,
                    current_value + request[parameter],
                )
        corresponding_advertiser_report.cost_per_clicks = (
            corresponding_advertiser_report.spend
            / corresponding_advertiser_report.clicks
        )
        corresponding_advertiser_report.cost_per_downloads = (
            corresponding_advertiser_report.spend
            / corresponding_advertiser_report.downloads
        )
        corresponding_advertiser_report.cost_per_installs = (
            corresponding_advertiser_report.spend
            / corresponding_advertiser_report.installs
        )
    else:
        new_report = AdvertiserReports(
            advertiser_id=advertiser_id,
            report_date=request["report_date"],
            impressions=request["impressions"],
            clicks=request["clicks"],
            cost_per_click=request["spend"] / request["clicks"],
            spend=request["spend"],
            downloads=request["downloads"],
            cost_per_download=request["spend"] / request["downloads"],
            installs=request["installs"],
            cost_per_install=request["spend"] / request["installs"],
        )
        db.session.add(new_report)
