from datetime import datetime, timedelta

from src.database.private.permissions import Permissions
from src.constants.permissions import (
    READ_ACCESS,
    WRITE_ACCESS,
    ADMIN_ACCESS,
    ADVERTISER_REPORTS,
    ADS_REPORTS,
    ADGROUPS_REPORTS,
    CAMPAIGNS_REPORTS,
)
from src.database.database_basis import db
from src.database.private.user import Users


class EndpointManagingHelper:
    def __init__(self):
        pass

    def get_user(self, user_id):
        return Users.query.filter_by(user_id=user_id).first()

    def lazy_delete(self, table):
        all_data = table.query.filter_by(status="DELETED")
        for campaign in all_data:
            delta = datetime.utcnow() - campaign.deletion_date
            if delta >= timedelta(days=7):
                db.session.delete(campaign)
        db.session.commit()

    def create_date_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y-%m-%d").strftime("%Y-%m-%d")

    def check_permissions(self, value, permission):
        return value & (1 << permission) == (1 << permission)

    def update_permissions(self, request, section):
        permissions = 0
        if "READ_ACCESS" in request[section]:
            permissions ^= 1 << READ_ACCESS
        if "WRITE_ACCESS" in request[section]:
            permissions ^= 1 << WRITE_ACCESS
        if "ADMIN_ACCESS" in request[section]:
            permissions ^= 1 << ADMIN_ACCESS
        return permissions

    def update_reports_permissions(self, request):
        permissions = 0
        if "ADVERTISER_REPORTS" in request["reports"]:
            permissions ^= 1 << ADVERTISER_REPORTS
        if "CAMPAIGNS_REPORTS" in request["reports"]:
            permissions ^= 1 << CAMPAIGNS_REPORTS
        if "ADGROUPS_REPORTS" in request["reports"]:
            permissions ^= 1 << ADGROUPS_REPORTS
        if "ADS_REPORTS" in request["reports"]:
            permissions ^= 1 << ADS_REPORTS
        return permissions

    def check_user_permissions(self, advertiser_id, permission, section):
        permissions = Permissions.query.filter_by(advertiser_id=advertiser_id).first()
        if not permissions:
            return False
        return self.check_permissions(permissions[section], permission)

    def check_admin_permissions(self, advertiser_id):
        permissions = Permissions.query.filter_by(advertiser_id=advertiser_id).first()
        if not permissions:
            return False
        return permissions["admin"] == 1
