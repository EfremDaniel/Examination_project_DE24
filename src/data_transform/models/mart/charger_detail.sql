with fact_c as (select * from {{ ref('fact_charger') }}),
charger as (select * from {{ ref('dim_charger') }}),
area as (select * from {{ ref('dim_area') }}),
geo as (select * from {{ ref('dim_geo') }})

select
    c.operator,
    c.owned_by,
    c.update_date,
    c.parking_type,
    c.parking_info,
    c.connector_type,
    c.connector_info,
    fc.connector_nr,
    fc.number_charging_points,
    fc.available_charging_points,
    a.area,
    g.municipality,
    g.county,
from 
    fact_c fc
left join charger c on fc.charger_id = c.charger_id
left join  area a on fc.area_id = a.area_id 
left join geo g on fc.geo_id = g.geo_id 
