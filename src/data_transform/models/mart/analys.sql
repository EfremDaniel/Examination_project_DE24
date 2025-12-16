with fact as (select * from {{ ref('fact') }}),
charger as (select * from {{ ref('dim_charger') }}),
locations as (select * from {{ ref('dim_location') }})

select
    c.operator,
    c.owned_by,
    c.updated_date,
    c.parking_type,
    c.parking_info,
    c.connector_type,
    c.connector_info,
    f.connector_nr,
    f.number_charging_points,
    f.available_charging_points,
    l.area,
    l.municipality,
    l.municipality_id,
    l.county,
    l.county_id
from 
    fact f
left join charger c on f.charger_id = c.charger_id
left join locations l on f.locations_id = l.locations_id