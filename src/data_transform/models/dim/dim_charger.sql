with csmd as (select * from {{ ref('src_csmd') }}),
       st as (select * from {{ ref('src_st') }}),
     conn as (select * from {{ ref('src_conn') }})

select
    {{ dbt_utils.generate_surrogate_key(['csmd.id', 'st.attrname', 'conn.attrname']) }} as charger_id,
    max(csmd.owned_by) as owned_by,
    max(csmd.operator) as operator,
    st.attrname as parking_type,
    max(st.trans) as parking_info,
    conn.attrname as connector_type,
    max(conn.trans) as connector_info

from csmd
left join
st on csmd.id = st.station_id
left join
conn on csmd.id = conn.station_id
group by charger_id, parking_type, connector_type
