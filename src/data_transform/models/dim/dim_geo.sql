with csmd as (select * from {{ ref('src_csmd') }}),
trafikanalys as (select * from {{ ref('src_trafikanalys') }}),


csmd_trafikanalys as (
    select trim(lower(municipality)) as municipality, trim(lower(county)) as county from csmd
    union
    select trim(lower(municipality)) as municipality, trim(lower(county)) as county from trafikanalys
)


select
    {{ dbt_utils.generate_surrogate_key(['municipality', 'county']) }} as geo_id,
    municipality,
    county
from csmd_trafikanalys ct
where exists (
    select 
    1
    from {{ ref('municipality_lan') }} ml 
    where ct.municipality = trim(lower(ml.kommun)) 
    and ct.county = trim(lower(ml.l_n))
)


