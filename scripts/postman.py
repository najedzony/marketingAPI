from datetime import datetime

import requests


# def send_post(url):
#     headers = {
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODE4MjQ5NSwianRpIjoiZjY3NGFlNGQtNmU0OS00M2MxLWJiOTctOGIyZjIyZmIyNDBkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6OSwibmJmIjoxNjY4MTgyNDk1LCJleHAiOjE2NjgxODMzOTV9.5UMb6tfQOnaqe92PK7iEK5ZFnRDuPf9JLYIpATZDmL0"
#     }
#     params = {
#         "campaign_name": "new_campaign3",
#         "status": "ENABLED",
#     }
#     response = requests.post(url, headers=headers, json=params)
#     print(response.text)

# def send_post(url):
#     params = {
#         "username": "username6",
#         "password": "password12345",
#     }
#     response = requests.post(url, json=params)
#     print(response.text)


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2OTA1NzI4OCwianRpIjoiMjcxOGI3NWMtNWQxYi00ZDM0LTk2NWYtYmY4OTgwMjZjNjU2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6OSwibmJmIjoxNjY5MDU3Mjg4LCJleHAiOjE2NjkwNTgxODh9.Yp3rJFlwA0YriubA8VzHNkwRaw5cDEesVMR6w34Wcio"


def refresh_token():
    url = "http://127.0.0.1:5000/api/v1/auth/refresh"
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODE4Mzk2NiwianRpIjoiYzQzYTg4NmYtMWY2Ni00NGExLWIwODMtZjg5NjU1MzI0NGQxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjksIm5iZiI6MTY2ODE4Mzk2NiwiZXhwIjoxNjcwNzc1OTY2fQ.lPSuUvCMkD-r2bd8Mf5Wh9ZIKWZVE8_3idNcbVBLf_c"
    }
    response = requests.post(url, headers=headers)
    print(response.text)


# refresh_token()


def add_campaign():
    url = "http://127.0.0.1:5000/api/v1/campaign/add"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "campaign_name": "new_campaign111",
        "status": "ENABLED",
        "total_budget": "100",
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# add_campaign()


def list_campaigns():
    url = "http://127.0.0.1:5000/api/v1/campaign/list"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(response.text)


# list_campaigns()


def update_campaign():
    url = "http://127.0.0.1:5000/api/v1/campaign/update"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"campaign_id": 5, "total_budget": 1500}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# update_campaign()


def delete_campaign():
    url = "http://127.0.0.1:5000/api/v1/campaign/delete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "campaign_id": 5,
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# delete_campaign()


def undelete_campaign():
    url = "http://127.0.0.1:5000/api/v1/campaign/undelete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"campaign_id": 1}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# undelete_campaign()


def add_adgroup():
    url = "http://127.0.0.1:5000/api/v1/adgroups/add"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "campaign_id": 6,
        "adgroup_name": "new_adgroup111",
        "status": "ENABLED",
        "total_budget": 100,
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# add_adgroup()


def get_adgroup():
    url = "http://127.0.0.1:5000/api/v1/adgroups/get"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"adgroup_id": 3}
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_adgroup()


def get_all_adgroups():
    url = "http://127.0.0.1:5000/api/v1/adgroups/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"campaign_id": 10}
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_all_adgroups()


def update_adgroup():
    url = "http://127.0.0.1:5000/api/v1/adgroups/update"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "adgroup_id": 2,
        "total_budget": 10000,
        "daily_budget": 100,
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# update_adgroup()


def delete_adgroup():
    url = "http://127.0.0.1:5000/api/v1/adgroups/delete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"adgroup_id": 2}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# delete_adgroup()


def undelete_adgroup():
    url = "http://127.0.0.1:5000/api/v1/adgroups/undelete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"adgroup_id": 3}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# undelete_adgroup()


def add_ad():
    url = "http://127.0.0.1:5000/api/v1/ads/add"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "adgroup_id": 4,
        "ad_name": "new_ad5",
        "status": "ENABLED",
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# add_ad()


def get_ad():
    url = "http://127.0.0.1:5000/api/v1/ads/get"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ad_id": 1}
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_ad()


def get_all_ads():
    url = "http://127.0.0.1:5000/api/v1/ads/list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"adgroup_id": 2}
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_all_ads()


def update_ad():
    url = "http://127.0.0.1:5000/api/v1/ads/update"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "ad_id": 1,
        "status": "DISABLED",
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# update_ad()


def delete_ad():
    url = "http://127.0.0.1:5000/api/v1/ads/delete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ad_id": 1}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# delete_ad()


def undelete_ad():
    url = "http://127.0.0.1:5000/api/v1/ads/undelete"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ad_id": 1}
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# undelete_ad()


def add_report():
    url = "http://127.0.0.1:5000/api/v1/uploadreport"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "ad_id": 4,
        "report_date": datetime(2022, 11, 20).date().strftime("%Y-%m-%d"),
        "impressions": 10,
        "clicks": 5,
        "spend": 5.15,
        "downloads": 1,
        "installs": 1,
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.text)


# add_report()


def get_advertiser_reports():
    url = "http://127.0.0.1:5000/api/v1/reports/advertiser"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "date_from": "2022-11-18",
        "date_to": "2022-11-20",
    }
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_advertiser_reports()


def get_campaigns_reports():
    url = "http://127.0.0.1:5000/api/v1/reports/campaigns"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "date_from": "2022-11-21",
        "date_to": "2022-11-21",
        # "group_by": "REPORT_DATE",
    }
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_campaigns_reports()


def get_adgroups_reports():
    url = "http://127.0.0.1:5000/api/v1/reports/adgroups"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "date_from": "2022-11-18",
        "date_to": "2022-11-20",
        # "group_by": "REPORT_DATE"
    }
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


# get_adgroups_reports()


def get_ads_reports():
    url = "http://127.0.0.1:5000/api/v1/reports/ads"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "date_from": "2022-11-18",
        "date_to": "2022-11-20",
        # "group_by": "REPORT_DATE",
    }
    response = requests.get(url, headers=headers, json=params)
    print(response.text)


get_ads_reports()

"""
{
  "user": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODIwNDYzMywianRpIjoiYzg2ZDU5MjAtZTlmYi00MGEyLThmNDMtZTI5NDkyNmJiMWRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6OSwibmJmIjoxNjY4MjA0NjMzLCJleHAiOjE2NjgyMDU1MzN9.vSMa8SfkPUfE3BMLLNTlgRac_0lQmv-FAF6ANd9PPV8",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODE4Mzk2NiwianRpIjoiYzQzYTg4NmYtMWY2Ni00NGExLWIwODMtZjg5NjU1MzI0NGQxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjksIm5iZiI6MTY2ODE4Mzk2NiwiZXhwIjoxNjcwNzc1OTY2fQ.lPSuUvCMkD-r2bd8Mf5Wh9ZIKWZVE8_3idNcbVBLf_c"
  }
}
"""
