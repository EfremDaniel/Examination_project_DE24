with csmd as (select * from {{ ref('src_csmd') }}),
       st as (select * from {{ ref('src_st') }}),
     conn as (select * from {{ ref('src_conn') }})

select
{{ dbt_utils.generate_surrogate_key(["csmd.id", "csmd.street"])}} as area_id,
{{ dbt_utils.generate_surrogate_key(['csmd.id', 'st.attrname', 'conn.attrname']) }} as charger_id,
{{ dbt_utils.generate_surrogate_key(['trim(lower(csmd.municipality))', 'trim(lower(csmd.county))']) }} as geo_id,
cast(csmd.number_charging_points as int) as number_charging_points,
cast(csmd.available_charging_points as int) as available_charging_points,
cast(csmd.updated as date) as update_date,
cast(csmd.created as date) as created_date,
cast(st.attrtypeid as int) as status_type_id,
cast(st.attrvalid as int) as status_attr_valid,
cast(conn.connector_nr as int) as connector_nr,
cast(conn.attrtypeid as int) as connector_type_id,
cast(conn.attrvalid as int) as connector_attr_valid
from csmd
left join
st on csmd.id = st.station_id
left join
conn on csmd.id = conn.station_id
