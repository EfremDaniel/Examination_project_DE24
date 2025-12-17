with tr as (select * from {{ ref('src_trafikanalys') }})

select
    {{ dbt_utils.generate_surrogate_key(["id", "fuel"]) }} as vehicle_id,
    max(car_in_traffic) as vehicle_in_traffic,
    fuel
from tr
group by vehicle_id, fuel
