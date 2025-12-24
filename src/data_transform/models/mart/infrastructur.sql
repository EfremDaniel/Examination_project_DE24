with ft_charger as (select * from {{ ref('fact_charger') }}),
    dm_geo as (select * from {{ ref('dim_geo') }}),
    ft_vehicle as (select * from {{ ref('fact_vehicle') }}),
    dm_vehicle as (select * from {{ ref('dim_vehicle_in_traffic') }}),
    ft_connector as (select * from {{ ref('fact_connector') }}),
    dm_connector as (select * from {{ ref('dim_connector_attribute_value') }}),


-- cte block to get kW in float, using macros convert all with kW
conn_kw as (
    select
        ft_conn.station_id,
        {{ kW('dm_conn.trans') }} as to_kw
    from ft_connector ft_conn
    left join dm_connector dm_conn on ft_conn.conn_id = dm_conn.conn_id
    where trim(lower(dm_conn.attribute_name)) = 'charging capacity'
),

-- cte block to get max kW per station 
station_max_kw as (
    select
        station_id,
        max(to_kw) as max_kw_station
    from conn_kw
    group by station_id
),

-- cte block to sum kW per municipality
kw_muni as (
    select 
        ch.geo_id,
        sum(smk.max_kw_station) as total_kw
    from (select distinct geo_id, station_id from ft_charger) ch
    left join station_max_kw smk on ch.station_id = smk.station_id
    group by ch.geo_id
),

-- cte block to get the latest year
latest_year as (
    select
        max(ft_vehicle.year) as "year"
    from
        ft_vehicle 
),

-- cte block to aggregat charger for each geo_id
charger_aggr as (
    select
        geo_id,
        count(distinct(station_id)) antal_ladd_stationer
    from ft_charger 
    group by geo_id
),

-- cte block to aggregate vehicle for each municipality
vehicle_aggr as (
    select
        ft_vehicle.geo_id,
        sum(dm_vehicle.vehicle_in_traffic) as total_vehicle
    from ft_vehicle
    left join latest_year ly on ft_vehicle.year = ly."year" 
    left join dm_vehicle on ft_vehicle.vehicle_id = dm_vehicle.vehicle_id
    group by ft_vehicle.geo_id
)

select 
    c_aggr.antal_ladd_stationer,
    v_aggr.total_vehicle,
    kw_muni.total_kw,
    dm_geo.municipality,
    dm_geo.county
from charger_aggr c_aggr 
left join vehicle_aggr v_aggr on c_aggr.geo_id = v_aggr.geo_id
left join dm_geo on c_aggr.geo_id = dm_geo.geo_id
left join kw_muni on kw_muni.geo_id = c_aggr.geo_id



