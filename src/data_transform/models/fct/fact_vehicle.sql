with ft_v as (select * from {{ ref('src_trafikanalys') }})

select 
    {{ dbt_utils.generate_surrogate_key(["id", "fuel"]) }} as vehicle_id,
    'year'
from ft_v