# Marketing API

## API documentation

This is documentation for Marketing API that was build for bachelors thesis. 

Note, that all parameres with * are mandatory.

### Some important information

Note, that when you delete campaign, all of the corresponding adgroups and ads are gonna get deleted too. Same when you delete an adgroup, corresponding ads will get deleted. When you delete some resource, you can still undelete it for 7 days. After that time, it will get deleted forever.

For every request except this for auth endpoint, you need to provide access token in header, for example:
```json 
{
    "Authentication": "Bearer your_secret_access_token"
}
```

Provide information for admin of API, which scopes you need. He will give you access to endpoints, that your account will be using.

Basic address: http://localhost/api/v1

### Auth

Enpoints used for authentication

#### POST /auth/authenticate

Schema:
*username -> string
*password -> string

Example:
```json
{
    "username": "username1",
    "password": "password123"
}
```

Example response:
```json
{
    "user": {
        "access_token": "some_secret_access_token",
        "refresh_token": "some_secret_refresh_token"
    }
}
```

#### POST /auth/refresh

Provide your refresh token in header.

Example response:
```json
{
    "access_token": "some_secret_access_token"
}
```


### Campaigns

Endpoints, that are used to manage campaigns

#### POST campaign/add

Scopes needed: WRITE_ACCESS on campaigns 

Schema:
*campaign_name -> string
total_budget -> integer
daily_budget -> integer
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "campaign_name": "my_campaign_1",
    "total_budget": 10000,
    "daily_budget": 150,
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Campaign created",
    "campaign": {
        "campaign_id": 12344321,
        "campaign_name": "my_campaign_1"
    }
}
```

#### GET campaign/get

Scopes needed: READ_ACCESS on campaigns 

Schema:
*campaign_id -> integer

Example:
```json
{
    "campaign_id": 12344321
}
```

Example response:
```json
{
    "campaign_id": 12344321,
    "campaign_name": "my_campaign_1",
    "total_budget": 10000,
    "daily_budget": 150,
    "creation_date": "2022-11-13 16:54:08.45384",
    "last_update_date": "2022-11-13 16:54:08.45384",
    "deletion_date": null,
    "status": "ENABLED"
}
```

#### GET campaign/list

Scopes needed: READ_ACCESS on campaigns 

Example response:
```json 
[
    {
        "campaign_id": 12344321,
        "campaign_name": "my_campaign_1",
        "total_budget": 10000,
        "daily_budget": 150,
        "creation_date": "2022-11-13 16:54:08.45384",
        "last_update_date": "2022-11-13 16:54:08.45384",
        "deletion_date": null,
        "status": "ENABLED"
    }
]
```

#### POST campaign/update

Scopes needed: WRITE_ACCESS on campaigns 

Schema:
*campaign_id -> integer
total_budget -> integer
daily_budget -> integer
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "campaign_name": 12344321,
    "total_budget": 10000,
    "daily_budget": 150,
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Campaign updated",
    "campaign": {
        "campaign_id": 12344321,
        "campaign_name": "my_campaign_1"
    }
}
```

#### POST campaign/delete

Scopes needed: ADMIN_ACCESS on campaigns 

Schema:
*campaign_id -> integer

Example:
```json
{
    "campaign_id": 12344321
}
```

Example response:
```json
{
    "message": "Campaign deleted",
    "campaign": {
        "campaign_id": 12344321
    }
}
```

#### POST campaign/undelete

Scopes needed: ADMIN_ACCESS on campaigns 

Schema:
*campaign_id -> integer

Example:
```json
{
    "campaign_id": 12344321
}
```

Example response:
```json
{
    "message": "Campaign undeleted",
    "campaign": {
        "campaign_id": 12344321
    }
}
```

### Adgroups

Endpoints, that are used to manage adgroups

#### POST adgroups/add

Scopes needed: WRITE_ACCESS on adgroups 

Schema:
*campaign_id -> integer
*adgroup_name -> string
total_budget -> integer
daily_budget -> integer
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "campaign_id": 12344321,
    "adgroup_name": "my_adgroup_1",
    "total_budget": 10000,
    "daily_budget": 150,
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Adgroup created",
    "campaign": {
        "adgroup_id": 234432,
        "adgroup_name": "my_adgroup_1",
        "campaign_id": 12344321
    }
}
```

#### GET adgroups/get

Scopes needed: READ_ACCESS on adgroups 

Schema:
*adgroup_id -> integer

Example:
```json
{
    "adgroup_id": 234432
}
```

Example response:
```json
{
    "campaign_id": 12344321,
    "adgroup_id": 234432,
    "adgroup_name": "my_adgroup_1",
    "total_budget": 10000,
    "daily_budget": 150,
    "creation_date": "2022-11-13 16:54:08.45384",
    "last_update_date": "2022-11-13 16:54:08.45384",
    "deletion_date": null,
    "status": "ENABLED"
}
```

#### GET adgroups/list

Scopes needed: READ_ACCESS on adgroups 

Example response:
```json 
[
    {
        "campaign_id": 12344321,
        "adgroup_id": 234432,
        "adgroup_name": "my_adgroup_1",
        "total_budget": 10000,
        "daily_budget": 150,
        "creation_date": "2022-11-13 16:54:08.45384",
        "last_update_date": "2022-11-13 16:54:08.45384",
        "deletion_date": null,
        "status": ENABLED
    }
]
```

#### POST adgroups/update

Scopes needed: WRITE_ACCESS on adgroups 

Schema:
*adgroup_id -> integer
total_budget -> integer
daily_budget -> integer
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "adgroup_id": 234432,
    "total_budget": 10000,
    "daily_budget": 150,
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Adgroup updated",
    "adgroup": {
        "adgroup_id": 234432,
        "adgroup_name": "my_adgroup_1"
    }
}
```

#### POST adgroups/delete

Scopes needed: ADMIN_ACCESS on adgroups 

Schema:
*adgroup_id -> integer

Example:
```json
{
    "adgroup_id": 234432
}
```

Example response:
```json
{
    "message": "Adgroup deleted",
    "adgroup": {
        "adgroup_id": 234432
    }
}
```

#### POST adgroups/undelete

Scopes needed: ADMIN_ACCESS on adgroups

Schema:
*adgroup_id -> integer

Example:
```json
{
    "adgroup_id": 234432
}
```

Example response:
```json
{
    "message": "Adgroup undeleted",
    "adgroup": {
        "adgroup_id": 234432
    }
}
```


### Ads

Endpoints, that are used to manage ads

#### POST ads/add

Scopes needed: WRITE_ACCESS on ads

Schema:
*adgroup_id -> integer
*ad_name -> string
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "adgroup_id": 234432,
    "ad_name": "my_ad_1",
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Ad created",
    "campaign": {
        "ad_id": 3443,
        "ad_name": "my_ad_1",
        "adgroup_id": 234432,
        "campaign_id": 12344321
    }
}
```

#### GET ads/get

Scopes needed: READ_ACCESS on ads

Schema:
*ad_id -> integer

Example:
```json
{
    "ad_id": 3443
}
```

Example response:
```json
{
    "campaign_id": 12344321,
    "adgroup_id": 234432,
    "ad_id": 3443,
    "ad_name": "my_ad_1",
    "creation_date": "2022-11-13 16:54:08.45384",
    "last_update_date": "2022-11-13 16:54:08.45384",
    "deletion_date": null,
    "status": "ENABLED"
}
```

#### GET ads/list

Scopes needed: READ_ACCESS on ads

Example response:
```json 
[
    {
        "campaign_id": 12344321,
        "adgroup_id": 234432,
        "ad_id": 3443,
        "ad_name": "my_ad_1",
        "creation_date": "2022-11-13 16:54:08.45384",
        "last_update_date": "2022-11-13 16:54:08.45384",
        "deletion_date": null,
        "status": ENABLED
    }
]
```

#### POST ads/update

Scopes needed: WRITE_ACCESS on ads

Schema:
*ad_id -> integer
*status -> ["ENABLED", "DISABLED"]

Example:
```json
{
    "ad_id": 3443,
    "status": "ENABLED"
}
```

Example response:
```json
{
    "message": "Ad updated",
    "ad": {
        "ad_id": 3443,
        "ad_name": "my_ad_1"
    }
}
```

#### POST ads/delete

Scopes needed: ADMIN_ACCESS on ads

Schema:
*ad_id -> integer

Example:
```json
{
    "ad_id": 3443
}
```

Example response:
```json
{
    "message": "Ad deleted",
    "ad": {
        "ad_id": 3443
    }
}
```

#### POST adgroups/undelete

Scopes needed: ADMIN_ACCESS on ads

Schema:
*ad_id -> integer

Example:
```json
{
    "ad_id": 3443
}
```

Example response:
```json
{
    "message": "Ad undeleted",
    "ad": {
        "ad_id": 3443
    }
}
```


#### Reports

Endpoints with reporting data

#### GET /reports/advertiser

Scopes needed: ADVERTISER_REPORTS

Schema:
*date_from -> string
*date_to -> string

Example:
```json
{
    "date_from": "2022-12-01",
    "date_to": "2022-12-01"
}
```

Example response:
```json
[
     {   
        "advertiser_id": 789789,
        "report_date": "2022-12-01",
        "impressions": 10,
        "clicks": 5,
        "cost_per_click": 2.0,
        "spend": 10,
        "downloads": 2,
        "cost_per_downloads": 5.0,
        "installs": 2,
        "cost_per_install": 5.0
     }
]
```

#### GET /reports/campaigns

Scopes needed: CAMPAIGNS_REPORTS

Schema:
*date_from -> string
*date_to -> string
group_by -> ["CAMPAIGN_ID", "REPORT_DATE"]

Example:
```json
{
    "date_from": "2022-12-01",
    "date_to": "2022-12-01",
    "group_by": "REPORT_DATE"
}
```

Example response:
```json
[
     {   
        "report_date": "2022-12-01",
        "impressions": 10,
        "clicks": 5,
        "cost_per_click": 2.0,
        "spend": 10,
        "downloads": 2,
        "cost_per_downloads": 5.0,
        "installs": 2,
        "cost_per_install": 5.0
     }
]
```

#### GET /reports/adgroups

Scopes needed: ADGROUPS_REPORTS

Schema:
*date_from -> string
*date_to -> string
group_by -> ["ADGROUP_ID", "REPORT_DATE"]

Example:
```json
{
    "date_from": "2022-12-01",
    "date_to": "2022-12-01",
    "group_by": "ADGROUP_ID"
}
```

Example response:
```json
[
     {   
        "adgroup_id": 234432,
        "impressions": 10,
        "clicks": 5,
        "cost_per_click": 2.0,
        "spend": 10,
        "downloads": 2,
        "cost_per_downloads": 5.0,
        "installs": 2,
        "cost_per_install": 5.0
     }
]
```

#### GET /reports/ads

Scopes needed: ADS_REPORTS

Schema:
*date_from -> string
*date_to -> string
group_by -> ["AD_ID", "REPORT_DATE"]

Example:
```json
{
    "date_from": "2022-12-01",
    "date_to": "2022-12-01",
    "group_by": "REPORT_DATE"
}
```

Example response:
```json
[
     {   
        "report_date": "2022-12-01",
        "impressions": 10,
        "clicks": 5,
        "cost_per_click": 2.0,
        "spend": 10,
        "downloads": 2,
        "cost_per_downloads": 5.0,
        "installs": 2,
        "cost_per_install": 5.0
     }
]
```

### ADMIN

Endpoints for admins of API
For all requests on this endpoints you need to have ADMIN access.

#### POST /auth/register

Schema:
*username -> string
*password -> string
permissions -> struct

permissions schema:
campaigns -> ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"]
adgroups -> ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"]
ads -> ["READ_ACCESS", "WRITE_ACCESS", "ADMIN_ACCESS"]

Example:
```json
{
    "username": "username1",
    "password": "password123",
    "permissions": {
        "campaigns": [
            "READ_ACCESS",
            "WRITE_ACCESS"
        ]
    }
}
```

Example response:
```json
{
    "message": "User created",
    "user": {
        "username": "username1",
        "advertiser_id": 123412123
    }
}
```

#### POST /uploadreport

Schema:
*ad_id -> integer
*report_date -> string
*impressions -> integer
*clicks -> integer
*spend -> number
*downloads -> integer
*installs -> integer


Example:
```json
{
    "ad_id": 3443,
    "report_date": "2022-12-01",
    "impressions": 10,
    "clicks": 5,
    "spend": 105.42,
    "downloads": 2,
    "installs": 2
}
```

Example response:
```json
{
    "message": "Report added"
}
```