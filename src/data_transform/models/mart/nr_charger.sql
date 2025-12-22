with fact_charger as (select * from {{ ref('fact_charger') }}),
    geo as (select * from {{ ref('dim_geo') }}),
    fact_connector as (select * from {{ ref('fact_connector') }}),
    connector as (select * from {{ ref('dim_connector_attribute_value') }}),

-- cte block useing case when to get station_id when it 1 and null when 0 
conn as (
  select
      station_id,
      max(
        case 
          when c.trans in (
            '250 kW DC', '350 kW DC', '225 kW DC', '62,5 kW DC', '500 kW DC', '400 kW DC', '75 kW DC', 
            '150 kW DC', '200 kW DC', '300 kW DC', '135 kW - 480VDC max 270A', 
            '100 kW - 500VDC max 200A', '180 kW DC', '175 kW DC'
          )
          then 1 else 0
        end
      ) as is_fast_laddpunkter
  from fact_connector fac 
  left join connector c on fac.conn_id = c.conn_id
  group by station_id
)

-- count distinct case when if 1 then return fc.station_id. More robust way to get ridd of duplicates. 
-- nullif: if count(distinct fc.station) is 0 then null if not output fc.station_id.
-- round_ round to 2 decimal. 
select
    count(distinct(fc.station_id)) as antal_ladd_stationer,
    count(distinct(fc.operator_id)) as antal_operator,
    sum(fc.number_charging_points) as laddpunkter,
    count(distinct case when conn.is_fast_laddpunkter = 1 then fc.station_id end) antal_snabb_ladd_stationer,
    g.municipality,
    g.county
from 
  fact_charger fc 
left join geo g on fc.geo_id = g.geo_id
left join conn on fc.station_id = conn.station_id
group by g.municipality, g.county

