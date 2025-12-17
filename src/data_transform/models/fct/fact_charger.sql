with csmd as (select * from {{ ref('src_csmd') }}),
       st as (select * from {{ ref('src_st') }}),
     conn as (select * from {{ ref('src_conn') }})

select
{{ dbt_utils.generate_surrogate_key(['municipality_id', 'county_id', 'id']) }} as location_id,
{{ dbt_utils.generate_surrogate_key(['csmd.id', 'st.attrname', 'conn.attrname']) }} as charger_id,
csmd.number_charging_points,
csmd.available_charging_points,
csmd.house_number,
st.attrtypeid as status_type_id,
st.attrvalid as status_attr_valid,
conn.connector_nr,
conn.attrtypeid as connector_type_id,
conn.attrvalid as connector_attr_valid,
from csmd
left join
st on csmd.id = st.station_id
left join
conn on csmd.id = conn.station_id

