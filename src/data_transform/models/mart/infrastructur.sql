with fact_charger as (select * from {{ ref('fact_charger') }}),
    geo as (select * from {{ ref('dim_geo') }}),
    fact_connector as (select * from {{ ref('fact_connector') }}),
    connector as (select * from {{ ref('dim_connector_attribute_value') }}),

conn as (
  select
    station_id,
    connector_nr,
    max(
      case when c.trans in ('250 kW DC', '350 kW DC', '225 kW DC', '62,5 kW DC', '500 kW DC', '400 kW DC', '75 KW DC', '150 kW DC', '200 kW DC', 'Mode 4', '300 kW DC', '135 kW - 480VDC max 270A', '100 kW - 500VDC max 200A', '180 kW DC', '175 kW DC')
      then 1 else 0
      end
    ) as is_fast
  from fact_connector fc
  left join connector c on fc.conn_id = c.conn_id
  group by station_id, connector_nr
)

select
    count(distinct(fc.csmd_id)) as antal_laddare,
    count(distinct(fc.operator_id)) as antal_operator,
    sum(fc.number_charging_points) as laddpunkter,
    g.municipality,
    g.county,
    sum(conn.is_fast) as antal_snabb_laddare
from 
  fact_charger fc 
left join geo g on fc.geo_id = g.geo_id
left join conn on fc.csmd_id = conn.station_id
group by g.municipality, g.county

