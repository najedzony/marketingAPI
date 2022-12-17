CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username varchar(50) NOT NULL UNIQUE,
    password varchar NOT NULL,
    advertiser_id int NOT NULL UNIQUE
);


CREATE TABLE campaigns (
    advertiser_id int NOT NULL,
    campaign_id SERIAL PRIMARY KEY,
    campaign_name varchar NOT NULL UNIQUE,
    total_budget int,
    daily_budget int,
    creation_date timestamp,
    last_update_date timestamp,
    deletion_date timestamp,
    status varchar NOT NULL
);


CREATE TABLE adgroups (
    advertiser_id int NOT NULL,
    campaign_id int NOT NULL,
    adgroup_id SERIAL PRIMARY KEY,
    adgroup_name varchar NOT NULL UNIQUE,
    total_budget int,
    daily_budget int,
    creation_date timestamp,
    last_update_date timestamp,
    deletion_date timestamp,
    status varchar NOT NULL
);


CREATE TABLE ads (
    advertiser_id int NOT NULL,
    campaign_id int NOT NULL,
    adgroup_id int NOT NULL,
    ad_id SERIAL PRIMARY KEY,
    ad_name varchar NOT NULL UNIQUE,
    creation_date timestamp,
    last_update_date timestamp,
    deletion_date timestamp,
    status varchar NOT NULL
);


CREATE TABLE advertiser_reports (
    id SERIAL PRIMARY KEY,
    advertiser_id int NOT NULL,
    report_date timestamp NOT NULL,
    impressions int,
    clicks int,
    cost_per_click float,
    spend float,
    downloads int,
    cost_per_download float,
    installs int,
    cost_per_install float
);


CREATE TABLE campaigns_reports (
    id SERIAL PRIMARY KEY,
    advertiser_id int NOT NULL,
    campaign_id int NOT NULL,
    campaign_name varchar NOT NULL,
    report_date timestamp NOT NULL,
    impressions int,
    clicks int,
    cost_per_click float,
    spend float,
    downloads int,
    cost_per_download float,
    installs int,
    cost_per_install float
);


CREATE TABLE adgroups_reports (
    id SERIAL PRIMARY KEY,
    advertiser_id int NOT NULL,
    campaign_id int NOT NULL,
    adgroup_id int NOT NULL,
    adgroup_name varchar NOT NULL,
    report_date timestamp NOT NULL,
    impressions int,
    clicks int,
    cost_per_click float,
    spend float,
    downloads int,
    cost_per_download float,
    installs int,
    cost_per_install float
);


CREATE TABLE ads_reports (
    id SERIAL PRIMARY KEY,
    advertiser_id int NOT NULL,
    campaign_id int NOT NULL,
    adgroup_id int NOT NULL,
    ad_id int NOT NULL,
    ad_name varchar NOT NULL,
    report_date timestamp NOT NULL,
    impressions int,
    clicks int,
    cost_per_click float,
    spend float,
    downloads int,
    cost_per_download float,
    installs int,
    cost_per_install float
);


CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    advertiser_id int NOT NULL,
    campaigns int NOT NULL,
    adgroups int NOT NULL,
    ads int NOT NULL,
    reports int NOT NULL,
    admin int
);
