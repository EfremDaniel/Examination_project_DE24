with tr as (select * from {{ ref('src_trafikanalys') }})

select
    {{ dbt_utils.generate_surrogate_key(["id", "fuel"]) }} as vehicle_id,
    max(cast(vehicle_in_traffic as int)) as vehicle_in_traffic,
    fuel
from tr
group by vehicle_id, fuel

