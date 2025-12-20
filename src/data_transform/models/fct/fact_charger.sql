with csmd as (select * from {{ ref('src_csmd') }})

select
csmd.id as csmd_id,
{{dbt_utils.generate_surrogate_key(['csmd.operator'])}} as operator_id,
{{ dbt_utils.generate_surrogate_key(['trim(lower(csmd.municipality))', 'trim(lower(csmd.county))']) }} as geo_id,
cast(csmd.number_charging_points as int) as number_charging_points,
cast(csmd.available_charging_points as int) as available_charging_points,
cast(csmd.updated as date) as update_date,
cast(csmd.created as date) as created_date
from csmd
where exists (
  select
  1
  from {{ ref('municipality_lan') }} ml 
  where trim(lower(csmd.municipality)) = trim(lower(ml.kommun))
  and trim(lower(csmd.county)) = trim(lower(ml.l_n))
)

