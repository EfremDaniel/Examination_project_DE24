with ft_v as (select * from {{ ref('src_trafikanalys') }})

select 
    {{ dbt_utils.generate_surrogate_key(["id", "fuel"]) }} as vehicle_id,
    {{ dbt_utils.generate_surrogate_key(['trim(lower(ft_v.municipality))', 'trim(lower(ft_v.county))']) }} as geo_id,
    cast(year as int) as year
from ft_v
where exists (
    select
    1
    from {{ ref('municipality_lan') }} ml 
    where trim(lower(ft_v.municipality)) = trim(lower(ml.kommun))
    and trim(lower(ft_v.county)) = trim(lower(ml.l_n))
)

