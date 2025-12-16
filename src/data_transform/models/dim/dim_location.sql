with csmd as (select * from {{ ref('src_csmd') }})

select
{{ dbt_utils.generate_surrogate_key(['municipality_id', 'county_id', 'id']) }} as id,
max(street),
max(name) as area,
municipality_id,
max(municipality),
county_id,
max(county),
from csmd
group by municipality_id, county_id, id