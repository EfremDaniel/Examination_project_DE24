with vt as (select * from {{ ref('dim_vehicle_in_traffic') }}),
    fact as (select * from {{ref ('fact_vehicle')}})

select
    vt.vehicle_id,
    fuel,
    geo_id,
    f.year

from fact f

left join vt on f.vehicle_id = vt.vehicle_id
