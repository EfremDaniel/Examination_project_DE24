with src_csmd as (select * from {{ ref('src_csmd') }})

select
    {{ dbt_utils.generate_surrogate_key(["id", "street"])}} as area_id,
    street,
    max(name) as area,
    max({{ fill_street_nr('house_number') }}) as house_number
from src_csmd
group by area_id, street 