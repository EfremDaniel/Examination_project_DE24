with csmd as (select * from {{ ref('src_csmd') }})

select
{{ dbt_utils.generate_surrogate_key(['municipality', 'county', 'id']) }} as geo_id,
municipality_id,
max(municipality) as municipality,
county_id,
max(county) as county,
from csmd
group by municipality_id, county_id, geo_id 