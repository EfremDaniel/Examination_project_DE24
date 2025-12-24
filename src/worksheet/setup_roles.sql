
USE ROLE USERADMIN;
SELECT current_role();


CREATE ROLE IF NOT EXISTS dlt_role;
CREATE ROLE IF NOT EXISTS dbt_role;
CREATE ROLE IF NOT EXISTS streamlit_role;

-- change to securityadmin

USE ROLE SECURITYADMIN;
SELECT current_role();
SELECT current_user();
GRANT ROLE dlt_role TO USER extract_data;
GRANT ROLE dlt_role TO USER efrem;
GRANT ROLE dlt_role TO USER MarcusArdenstedt;



-- grant privileges to dlt_role
GRANT USAGE ON WAREHOUSE charger_station TO ROLE dlt_role;

GRANT USAGE ON DATABASE charger_station_vehicle TO ROLE dlt_role;

GRANT USAGE ON SCHEMA charger_station_vehicle.staging TO ROLE dlt_role;

GRANT CREATE TABLE ON SCHEMA charger_station_vehicle.staging TO ROLE dlt_role;


-- grant CRUD TO role dlt_role

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA charger_station_vehicle.staging TO ROLE dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA charger_station_vehicle.staging TO ROLE dlt_role;


-- check grants

SHOW GRANTS ON SCHEMA charger_station_vehicle.staging;

SHOW FUTURE GRANTS IN SCHEMA charger_station_vehicle.staging;

SHOW GRANTS TO ROLE dlt_role;

SHOW GRANTS TO USER extract_data; 

-- grant privileges to role dbt_role 

GRANT USAGE ON WAREHOUSE charger_station To dbt_role;

GRANT ROLE dbt_role TO USER transform_data;

GRANT USAGE ON DATABASE charger_station_vehicle TO dbt_role;
GRANT USAGE ON SCHEMA charger_station_vehicle.warehouse TO dbt_role;
GRANT USAGE ON SCHEMA charger_station_vehicle.staging TO dbt_ROLE;

GRANT CREATE TABLE ON SCHEMA charger_station_vehicle.warehouse TO dbt_role;
GRANT CREATE TABLE ON SCHEMA charger_station_vehicle.staging TO dbt_role;

GRANT CREATE VIEW ON SCHEMA charger_station_vehicle.warehouse TO dbt_role;
GRANT CREATE VIEW ON SCHEMA charger_station_vehicle.staging TO dbt_role;

-- grant crud to role dbt role
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA charger_station_vehicle.staging TO ROLE dbt_role;
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA charger_station_vehicle.staging TO ROLE dbt_role;
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA charger_station_vehicle.warehouse TO ROLE dbt_role;
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA charger_station_vehicle.warehouse TO ROLE dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA charger_station_vehicle.staging TO ROLE dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA charger_station_vehicle.warehouse TO ROLE dbt_role;

GRANT CREATE TABLE ON SCHEMA charger_station_vehicle.marts TO ROLE dbt_role;
GRANT CREATE VIEW ON SCHEMA charger_station_vehicle.marts TO ROLE dbt_role;
GRANT USAGE ON SCHEMA charger_station_vehicle.marts TO ROLE dbt_role;


-- grant role to useradmin
GRANT ROLE dbt_role TO USER efrem;
GRANT ROLE dbt_role TO USER MarcusArdenstedt;


-- grant privileges to role 
USE ROLE SECURITYADMIN;

GRANT USAGE ON WAREHOUSE charger_station TO ROLE streamlit_role;

GRANT USAGE ON DATABASE charger_station_vehicle TO ROLE streamlit_role;

GRANT USAGE ON SCHEMA charger_station_vehicle.marts TO ROLE streamlit_role;

GRANT SELECT ON ALL TABLES IN SCHEMA charger_station_vehicle.marts TO ROLE streamlit_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA charger_station_vehicle.marts TO ROLE streamlit_role;

GRANT SELECT ON ALL VIEWS IN SCHEMA charger_station_vehicle.marts TO ROLE streamlit_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA charger_station_vehicle.marts TO ROLE streamlit_role;

GRANT ROLE streamlit_role TO USER present_data;

GRANT role streamlit_role TO USER efrem;
GRANT ROLE streamlit_role TO USER MarcusArdenstedt;