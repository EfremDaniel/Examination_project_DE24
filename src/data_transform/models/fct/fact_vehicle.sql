with ft_v as (select * from {{ ref('src_trafikanalys') }})

select 
    {{ dbt_utils.generate_surrogate_key(["id", "fuel"]) }} as vehicle_id,
    {{ dbt_utils.generate_surrogate_key(['trim(lower(ft_v.municipality))', 'trim(lower(ft_v.county))']) }} as geo_id,
    cast(year as int) as year
from ft_v

