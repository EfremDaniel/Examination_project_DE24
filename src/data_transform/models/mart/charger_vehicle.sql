with v_i_t as (select * from {{ ref('dim_vehicle_in_traffic') }}),
    fact_v as (select * from {{ ref ('fact_vehicle') }}),
    geo as (select * from {{ ref('dim_geo') }}),
    fact_c as (select * from {{ ref('fact_charger') }}),
    ch as (select * from {{ ref('dim_charger') }})
    
select
    v_i_t.vehicle_id,
    v_i_t.fuel,
    g.municipality,
    g.county,
    fv.year,
    ch.operator,
    ch.parking_type,
    ch.parking_info,
    ch.connector_type,
    ch.connector_info,
    fc.created_date,
    fc.update_date
from fact_v fv
inner join v_i_t on fv.vehicle_id = v_i_t.vehicle_id
inner join geo g on fv.geo_id = g.geo_id
inner join fact_c fc on g.geo_id = fc.geo_id
inner join ch ch on fc.charger_id = ch.charger_id


