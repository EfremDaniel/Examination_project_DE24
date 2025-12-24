USE ROLE SYSADMIN;

SELECT current_role();

CREATE WAREHOUSE IF NOT EXISTS charger_station
WITH 
WAREHOUSE_SIZE="XSMALL"
AUTO_SUSPEND= 60
AUTO_RESUME= TRUE
INITIALLY_SUSPENDED= TRUE
COMMENT= "Warehouse for examination project for analyze data from NOBIL";

CREATE DATABASE IF NOT EXISTS charger_station_vehicle;

CREATE SCHEMA IF NOT EXISTS charger_station_vehicle.staging;



-- create schema for warehouse and marts

CREATE SCHEMA IF NOT EXISTS charger_station_vehicle.warehouse;

CREATE SCHEMA IF NOT EXISTS charger_station_vehicle.marts;