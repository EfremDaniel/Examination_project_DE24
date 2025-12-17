with csmd as (select * from {{ ref('src_csmd') }})

select
{{ dbt_utils.generate_surrogate_key(['municipality_id', 'county_id', 'id']) }} as location_id,
max(street) as street,
max(name) as area,
municipality_id,
max(municipality) as municipality,
county_id,
max(county) as county,
from csmd
group by municipality_id, county_id, location_id